[[Japanese](https://github.com/Kazuhito00/IPNE-YouTube-Input-Node)/English] 

> [!WARNING]
> IPNE-YouTube-Input-Node is an additional node for [Image-Processing-Node-Editor](https://github.com/Kazuhito00/Image-Processing-Node-Editor). <br>
> This repository alone does not work.

# IPNE-YouTube-Input-Node
It is a node for YouTube input that works with [Image-Processing-Node-Editor](https://github.com/Kazuhito00/Image-Processing-Node-Editor).

https://user-images.githubusercontent.com/37477845/179127642-0cb68f07-3a64-43e0-a870-563bdd8c2034.mp4

# Requirement
In addition to the dependent packages of [Image-Processing-Node-Editor](https://github.com/Kazuhito00/Image-Processing-Node-Editor), the following packages need to be installed.
```
pip install -U yt-dlp
pip install git+https://github.com/Kazuhito00/pafy
```

# Installation
Copy "node/input_node/node_youtube_input.py" to "[node/input_node](https://github.com/Kazuhito00/Image-Processing-Node-Editor/tree/main/node/input_node)" of [Image-Processing-Node-Editor](https://github.com/Kazuhito00/Image-Processing-Node-Editor).

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
            Node that reads YouTube and outputs images<br>
            Please specify the URL of the YouTube video in the URL field and press the "Start" button<br>
            It will take some time before playback starts<br>
            Specify the YouTube loading interval with "Interval(ms)"
        </td>
    </tr>
</table>

</details>

# Author
Kazuhito Takahashi(https://twitter.com/KzhtTkhs)
 
# License 
IPNE-YouTube-Input-Node is under [Apache-2.0 license](LICENSE).<br><br>
