<h3 align="center">

[![Download][download-shield]][download-url]
[![Release][release-shield]][release-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]
</h3>

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/phamngocvinh/py-checksum">
    <img src="images/icons/icon-192x192.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">PyChecksum</h3>

  <p align="center">
    :shield: Create and verify files hashes with one click
    <br />
    <a href="https://github.com/phamngocvinh/py-checksum"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/phamngocvinh/py-checksum/wiki/Usage-Example">View Demo</a>
    ·
    <a href="https://github.com/phamngocvinh/py-checksum/issues">Report Bug</a>
    ·
    <a href="https://github.com/phamngocvinh/py-checksum/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#stars-about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#beginner-how-to-build">How to Build</a>
    </li>
    <li><a href="#man_teacher-usage">Usage</a></li>
    <li><a href="#world_map-roadmap">Roadmap</a></li>
    <li><a href="#rocket-contributing">Contributing</a></li>
    <li><a href="#closed_book-license">License</a></li>
    <li><a href="#mailbox-contact">Contact</a></li>
    <li><a href="#books-acknowledgements">Acknowledgements</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## :stars: About The Project

PyChecksum is used to automatically generate and verify multiple files hash with the most popular algorithms

<!-- HOW TO BUILD -->
## :beginner: How to Build

To get a local copy up and running, follow these simple steps.

1. Clone the repo
   ```sh
   git clone https://github.com/phamngocvinh/py-checksum.git
   ```
2. Install requirements
   ```sh
   pip install -r requirements.txt
   ```
3. Run `build` script
4. Executable file will be generated in `dist` folder

<!-- USAGE -->
## :man_teacher: Usage
1. The first time you run, it will generate a hash for all file in the current folder (include sub-folder).
2. `PyChecksum.hash` containing all file's hashes will be generated.
3. Any time `PyChecksum.hash` exists, if you run again, it will check the current folder file's hash with hash in `PyChecksum.hash`
4. `PyCheckResult.txt` containing check result will be generated.

_For more examples, please refer to the [Documentation](https://github.com/phamngocvinh/py-checksum/wiki)_

<!-- ROADMAP -->
## :world_map: Roadmap

See the [open issues](https://github.com/phamngocvinh/py-checksum/issues) for a list of proposed features (and known issues).

<!-- CONTRIBUTING -->
## :rocket: Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## :closed_book: License

Distributed under the GPL-3.0 License. See `LICENSE` for more information.

<!-- CONTACT -->
## :mailbox: Contact

[![Mail][mail-shield]][mail-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- ACKNOWLEDGEMENTS -->
## :books: Acknowledgements

* [Python Software Foundation](https://www.python.org/)
* [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/)
* [Shields.io](https://shields.io)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[download-shield]: https://img.shields.io/github/downloads/phamngocvinh/py-checksum/total?style=for-the-badge&labelColor=4c566a&color=5e81ac&logo=github&logoColor=white
[download-url]: https://github.com/phamngocvinh/py-checksum/releases/latest
[release-shield]: https://img.shields.io/github/v/release/phamngocvinh/py-checksum?style=for-the-badge&labelColor=4c566a&color=5e81ac&logo=Battle.net&logoColor=white
[release-url]: https://github.com/phamngocvinh/py-checksum/releases/latest
[issues-shield]: https://img.shields.io/github/issues/phamngocvinh/py-checksum?style=for-the-badge&labelColor=4c566a&color=5e81ac&logo=Todoist&logoColor=white
[issues-url]: https://github.com/phamngocvinh/py-checksum/issues
[license-shield]: https://img.shields.io/github/license/phamngocvinh/py-checksum?style=for-the-badge&labelColor=4c566a&color=5e81ac&logo=AdGuard&logoColor=white
[license-url]: https://github.com/phamngocvinh/py-checksum/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/linkedin-blue?style=for-the-badge&logo=linkedin
[linkedin-url]: https://www.linkedin.com/in/phamngocvinh932
[mail-shield]: https://img.shields.io/badge/Gmail-white?style=for-the-badge&logo=gmail
[mail-url]: mailto:phamngocvinh@live.com
[product-screenshot]: images/screenshot.jpg
