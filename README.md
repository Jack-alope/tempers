# Rianú 

This project is called `rianú`, the Irish Language word for tracking. 

Rianú is an open source software, released under the BSD 3-Clause License, designed to more efficiently track engineered cardiac tissues. For further information on installation, setup, and customization please visit [rianu.mrph.dev](https://rianu.mrph.dev).

[![Website](https://img.shields.io/website?down_color=red&down_message=offline&label=docs&style=flat&up_color=success&up_message=online&url=https://rianu.mrph.dev)](https://rianu.mrph.dev)
[![paper doi](https://img.shields.io/badge/paper%20doi-manuscript%20in%20preparation-blue)](https://gitlab.com/hect-software/rianu)
[![project doi](https://img.shields.io/badge/project%20doi-10.17605/OSF.IO/YWCHZ-blue)](https://doi.org/10.17605/OSF.IO/YWCHZ)
[![pylint](https://hect-software.gitlab.io/rianu/badges/pylint.svg)](https://hect-software.gitlab.io/rianu/lint/)
[![pipeline status](https://gitlab.com/hect-software/rianu/badges/main/pipeline.svg)](https://gitlab.com/hect-software/rianu/commits/main)


## Pronunciation  
![](https://storageapi.fleek.co/jack-alope-team-bucket/Rianú.mp3)
_Pronunciation kindly supplied by a native corkonian._

## Citation  

If you use this software in research we kindly ask that you cite it as:  
```bibtex
@article{MurphyRianu2021,
    author = {Jack F. Murphy and Kevin D. Costa and Irene C. Turnbull},
    journal = {Manuscript in preparation},
    title = {Rianú: Multi-tissue tracking software for increased throughput of engineered cardiac tissue screening},
}
```  

## Installation
This software can be deployed on any machine, as long as Docker is preinstalled, however it is recommended to deploy on a cloud server. The setup below if for a public instance, not password protected. Password protection is possible through a slightly more involved installation process that will be added.

---

##### Instructions for Digital Ocean
1. Create a droplet, for image choose Docker from marketplace tab. 
2. Choose any CPU plan, the more cores the better. Lower plans will still work but be much slower. 
3. Under additional options select `User Data`. Copy and paste the following bash script.
    ```sh
    #!/bin/bash
    wget https://gitlab.com/hect-software/rianu/-/raw/main/docker-compose.yml -P /root/
    docker-compose -f /root/docker-compose.yml up -d
    ```
4. Create droplet. It takes a while (~5-10 mins) to install so take a break, grab some coffee. 
5. Access the droplet via `http://IP-OF-DROPLET/`. Note that just because the droplet says it is up and gives an ip address does not mean it has finished installing. So if `http://IP-OF-DROPLET/` does not resolve just wait a few more minutes.

---

##### Instructions to build from source
If the docker images are not working you can build your own from source. 
1. Clone this repository, and cd into the root of the directory
2. Build from source using this command.  
    ```sh
    docker-compose -f docker-compose-build.yml up -d
    ```
3. Access via web browser. If built on your local machine, `http://localhost/`. If on server, `http://IP-OF-SERVER/`.

## Usage  

##### Important notes
Tracking:
- If calibration distance is selected. Draw box for calibration, followed by a box for each tissues cross section, and lastly a box for each post. 
- If calibration set is selected or calibration factor inputted, no box is drawn for calibration.
- For the calibration distance and cross section distance the distance used is the euclidian distance between the first click and second click of the mouse (diagonal of the box).
- The difference between the centroid of box locations is taken in pairs to measure contraction (boxes 1-2; 3-4; 5-6; n-n+1). This means boxes should be drawn in the following order: left post of tissue 1 --> right post of tissue 1 --> left post of tissue 2 --> right post if tissue 2  --> left post of tissue n --> right post of tissue n. This is also because the first box drawn for each tissue (boxes 1,3,5,n) relates to the left height entry in the bioreactor database while the second box for each tissue (boxes 2,3,6,n+1) relate to the right post, so in order to get accurate force measurements this convention must be followed. 
- Tracking takes a while, and until the video is finished tracking analysis of those tissues will show up blank. You can do other things like database editing while tracking is running but it may be slower (depends on how powerful computer is).

Analysis:
- If the data does not auto-smooth and find points right away this means it failed to detect peaks. Try these fixes in the following order: Lower the threshold slider --> Lower the buffer slider --> Lower the minimum distance slider.

## Contributing  
  
If you are a member of a lab with a different bioreactor setup or have different analysis needs and would like to contribute to this repository please see [`contributing.md`](https://gitlab.com/hect-software/rianu/-/blob/main/CONTRIBUTING.md) for instruction on how to setup for development. Alternatively, open and issue on this repository or email `jack@mrph.dev` and I can work to add support for your system. We are very open to collaboration and want this software to be applicable to as many systems as possible.

---

