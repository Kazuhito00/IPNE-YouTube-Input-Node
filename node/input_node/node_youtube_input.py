#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

import cv2
import pafy
import numpy as np
import dearpygui.dearpygui as dpg

from node_editor.util import dpg_get_value, dpg_set_value

from node.node_abc import DpgNodeABC
from node_editor.util import convert_cv_to_dpg


class Node(DpgNodeABC):
    _ver = '0.0.1'

    node_label = 'YouTube'
    node_tag = 'YouTubeInput'

    _opencv_setting_dict = None
    _start_label = 'Start'
    _stop_label = 'Stop'
    _loading_label = 'Loading...'

    _wait_interval = 50  # ms

    _youtube_capture = {}
    _prev_read_time = {}

    def __init__(self):
        pass

    def add_node(
        self,
        parent,
        node_id,
        pos=[0, 0],
        opencv_setting_dict=None,
        callback=None,
    ):
        # タグ名
        tag_node_name = str(node_id) + ':' + self.node_tag
        tag_node_input01_name = tag_node_name + ':' + self.TYPE_TEXT + ':Input01'
        tag_node_input01_value_name = tag_node_name + ':' + self.TYPE_TEXT + ':Input01Value'
        tag_node_output01_name = tag_node_name + ':' + self.TYPE_IMAGE + ':Output01'
        tag_node_output01_value_name = tag_node_name + ':' + self.TYPE_IMAGE + ':Output01Value'
        tag_node_output02_name = tag_node_name + ':' + self.TYPE_TIME_MS + ':Output02'
        tag_node_output02_value_name = tag_node_name + ':' + self.TYPE_TIME_MS + ':Output02Value'

        tag_node_button_name = tag_node_name + ':' + self.TYPE_TEXT + ':Button'
        tag_node_button_value_name = tag_node_name + ':' + self.TYPE_TEXT + ':ButtonValue'

        # OpenCV向け設定
        self._opencv_setting_dict = opencv_setting_dict
        small_window_w = self._opencv_setting_dict['input_window_width']
        small_window_h = self._opencv_setting_dict['input_window_height']
        use_pref_counter = self._opencv_setting_dict['use_pref_counter']

        # 初期化用黒画像
        black_image = np.zeros((small_window_w, small_window_h, 3))
        black_texture = convert_cv_to_dpg(
            black_image,
            small_window_w,
            small_window_h,
        )

        # テクスチャ登録
        with dpg.texture_registry(show=False):
            dpg.add_raw_texture(
                small_window_w,
                small_window_h,
                black_texture,
                tag=tag_node_output01_value_name,
                format=dpg.mvFormat_Float_rgb,
            )

        # ノード
        with dpg.node(
                tag=tag_node_name,
                parent=parent,
                label=self.node_label,
                pos=pos,
        ):
            # YouTube URL入力欄
            with dpg.node_attribute(
                    tag=tag_node_input01_name,
                    attribute_type=dpg.mvNode_Attr_Static,
            ):
                dpg.add_input_text(
                    tag=tag_node_input01_value_name,
                    label='URL',
                    width=small_window_w - 30,
                )
            # カメラ画像
            with dpg.node_attribute(
                    tag=tag_node_output01_name,
                    attribute_type=dpg.mvNode_Attr_Output,
            ):
                dpg.add_image(tag_node_output01_value_name)
            # 録画/再生追加ボタン
            with dpg.node_attribute(
                    tag=tag_node_button_name,
                    attribute_type=dpg.mvNode_Attr_Static,
            ):
                dpg.add_button(
                    label=self._start_label,
                    tag=tag_node_button_value_name,
                    width=small_window_w,
                    callback=self._button,
                    user_data=tag_node_name,
                )
            # 処理時間
            if use_pref_counter:
                with dpg.node_attribute(
                        tag=tag_node_output02_name,
                        attribute_type=dpg.mvNode_Attr_Output,
                ):
                    dpg.add_text(
                        tag=tag_node_output02_value_name,
                        default_value='elapsed time(ms)',
                    )

        return tag_node_name

    def update(
        self,
        node_id,
        connection_list,
        node_image_dict,
        node_result_dict,
    ):
        tag_node_name = str(node_id) + ':' + self.node_tag
        input_value01_tag = tag_node_name + ':' + self.TYPE_TEXT + ':Input01Value'
        output_value01_tag = tag_node_name + ':' + self.TYPE_IMAGE + ':Output01Value'
        output_value02_tag = tag_node_name + ':' + self.TYPE_TIME_MS + ':Output02Value'

        small_window_w = self._opencv_setting_dict['input_window_width']
        small_window_h = self._opencv_setting_dict['input_window_height']
        use_pref_counter = self._opencv_setting_dict['use_pref_counter']

        # YouTube URL取得
        youtube_url = dpg_get_value(input_value01_tag)

        # VideoCapture()インスタンス取得
        youtube_capture = None
        if youtube_url != '':
            if youtube_url in self._youtube_capture:
                youtube_capture = self._youtube_capture[youtube_url]

        # 計測開始
        if youtube_url != '' and use_pref_counter:
            start_time = time.perf_counter()

        # 画像取得
        frame = None
        if youtube_capture is not None:
            ret = False

            if youtube_url not in self._prev_read_time:
                ret, frame = youtube_capture.read()
            else:
                interval_time = start_time - self._prev_read_time[youtube_url]
                interval_time = int(interval_time * 1000)
                if interval_time > self._wait_interval:
                    ret, frame = youtube_capture.read()

            if not ret:
                return None, None

            self._prev_read_time[youtube_url] = start_time

        # 計測終了
        if youtube_url != '' and use_pref_counter:
            elapsed_time = time.perf_counter() - start_time
            elapsed_time = int(elapsed_time * 1000)
            dpg_set_value(output_value02_tag,
                          str(elapsed_time).zfill(4) + 'ms')

        # 描画
        if frame is not None:
            texture = convert_cv_to_dpg(
                frame,
                small_window_w,
                small_window_h,
            )
            dpg_set_value(output_value01_tag, texture)

        return frame, None

    def close(self, node_id):
        pass

    def get_setting_dict(self, node_id):
        tag_node_name = str(node_id) + ':' + self.node_tag
        tag_node_input01_value_name = tag_node_name + ':' + self.TYPE_TEXT + ':Input01Value'

        pos = dpg.get_item_pos(tag_node_name)
        youtube_url = dpg_get_value(tag_node_input01_value_name)

        setting_dict = {}
        setting_dict['ver'] = self._ver
        setting_dict['pos'] = pos
        setting_dict[tag_node_input01_value_name] = youtube_url

        return setting_dict

    def set_setting_dict(self, node_id, setting_dict):
        tag_node_name = str(node_id) + ':' + self.node_tag
        tag_node_input01_value_name = tag_node_name + ':' + self.TYPE_TEXT + ':Input01Value'

        youtube_url = setting_dict[tag_node_input01_value_name]

        dpg_set_value(tag_node_input01_value_name, youtube_url)

    def _button(self, sender, data, user_data):
        tag_node_name = user_data
        input_value01_tag = tag_node_name + ':' + self.TYPE_TEXT + ':Input01Value'
        tag_node_button_value_name = tag_node_name + ':' + self.TYPE_TEXT + ':ButtonValue'

        label = dpg.get_item_label(tag_node_button_value_name)

        # RTSP URL取得
        youtube_url = dpg_get_value(input_value01_tag)

        if label == self._start_label:
            if youtube_url != '':
                if not (youtube_url in self._youtube_capture):
                    dpg.set_item_label(tag_node_button_value_name,
                                       self._loading_label)

                    pafy_video = pafy.new(youtube_url)
                    pafy_best_video = pafy_video.getbest(preftype="mp4")
                    youtube_capture = cv2.VideoCapture(pafy_best_video.url)
                    self._youtube_capture[youtube_url] = youtube_capture

                    dpg.set_item_label(tag_node_button_value_name,
                                       self._stop_label)
        elif label == self._stop_label:
            if youtube_url != '':
                if youtube_url in self._youtube_capture:
                    self._youtube_capture[youtube_url].release()
                    del self._youtube_capture[youtube_url]

            dpg.set_item_label(tag_node_button_value_name, self._start_label)
