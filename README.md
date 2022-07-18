[Japanese/[English](README_EN.md)]

> **Warning** <br>
> IPNE-YouTube-Input-Node は [Image-Processing-Node-Editor](https://github.com/Kazuhito00/Image-Processing-Node-Editor) の追加用ノードです。<br>
> このリポジトリ単体では動作しません。

# IPNE-YouTube-Input-Node
[Image-Processing-Node-Editor](https://github.com/Kazuhito00/Image-Processing-Node-Editor) で動作するYouTube入力用ノードです。

https://user-images.githubusercontent.com/37477845/179127642-0cb68f07-3a64-43e0-a870-563bdd8c2034.mp4

# Requirement
[Image-Processing-Node-Editor](https://github.com/Kazuhito00/Image-Processing-Node-Editor) の依存パッケージに加えて、以下のパッケージのインストールが必要です。
```
pip install -U yt-dlp
pip install git+https://github.com/Kazuhito00/pafy
```

# Installation
「node/input_node/node_youtube_input.py」を <br>
[Image-Processing-Node-Editor](https://github.com/Kazuhito00/Image-Processing-Node-Editor) の 「[node/input_node](https://github.com/Kazuhito00/Image-Processing-Node-Editor/tree/main/node/input_node)」にコピーしてください。

# Node
<details open>
<summary>Input Node</summary>

<table>
    <tr>
        <td width="200">
            YouTube
        </td>
        <td width="320">
            <img src="https://user-images.githubusercontent.com/37477845/179450682-f7cc8237-e9d8-4c0f-b5d8-d2caac453f04.png" loading="lazy" width="300px">
        </td>
        <td width="760">
            YouTubeを読み込み、画像を出力するノード<br>
            URL欄にYouTube動画のURLを指定して「Start」ボタンを押してください<br>
            再生が始まるまでに少々時間がかかります<br>
            Interval(ms)でYouTube読み込み間隔を指定します
        </td>
    </tr>
</table>

</details>

# Author
高橋かずひと(https://twitter.com/KzhtTkhs)
 
# License 
Image-Processing-Node-Editor is under [Apache-2.0 license](LICENSE).<br><br>
