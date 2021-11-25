<div id="top"></div>

[![Contributors][contributors-shield]][contributors-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
  <h3 align="center">Musicoop</h3>

  <p align="center">
    Musicoop é uma rede social onde pessoas ajudam outras pessoas a construir música!
    <br />
    <a href="https://musicoop-api.herokuapp.com/docs"><strong> Documentação »</strong></a>
    <br />
    ·
    <a href="https://github.com/felipemaia02/musicoop/issues">Reportar Bug</a>
  </p>
</div>

<!-- ABOUT THE PROJECT -->

## Sobre o projeto

No mundo da programação é muito comum se deparar com projetos OpenSource onde a comunidade de programadores estão sempre se ajudando a construir cada vez melhores projetos e ideias. Com isso a ideia do projeto é levar a mesma ideia de colaboração para mundo da arte principalmente a música, com isso estamos desenvolvendo uma aplicação para que isso possa acontecer. Um lugar onde pessoas independente de experiência, ajudam outros pessoas a fazerem música. Basta ter uma ideia!

A plataforma não fica apenas limitada a criação de músicas mas podendo compartilhamento dos projetos. Com isso estamos construindo o Musicoop!

<p align="right">(<a href="#top">back to top</a>)</p>

### Tecnlogias usadas

Esse repositório é da nossa API, ela foi construida usando Python com FastAPI e estamos usando o Postgres como banco de dados.

- [Python](https://www.python.org/)
- [Postgres](https://www.postgresql.org/)
- [FastAPI](https://fastapi.tiangolo.com/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Começando

Nosso projeto pode ser executado de duas maneiras poetry ou docker cabe a você escolher qual usar.

Uma maneira é usando o poetry, os passos abaixo é o recomendado para seguir:

### Instalação Poetry

Aqui você precisa instalar o poetry, você pode seguir a documentação de instalação do poetry <a href="https://python-poetry.org/docs/#installation"> aqui</a> ou seguir o caminho abaixo, precisa também instalar o <a href="https://www.postgresql.org/download/"> Postgres</a>, siga as instalações do seu sistema operacional.

- Poetry

  ```sh
  pip install --user poetry
  ```

  ou

  ```sh
  pip3 install --user poetry
  ```

### Instalação

_Aqui são os passos de instalação e inicialização do servidor de desenvolvimento usando docker ou poetry com uvicorn._

1. Clone do repositorio

   ```sh
   git clone https://github.com/felipemaia02/musicoop.git
   ```

2. Criar um arquivo .env dentro da pasta raiz do projeto e copiar o conteúdo que está dentro da dev.env e colocar no .env. e colocar suas credenciais do postgres na variavel SQLALCHAMY_DATABASE_URL e trocar os campos USER,PASSWORD e IP
   ```
   SQLALCHAMY_DATABASE_URL=postgresql://USER:PASSWORD@IP:5432/musicoop
   ```

- Aqui caso esteja usando o poetry:

  3. Ativar ambiente do poetry

     ```sh
     poetry shell
     ```

  4. Instalar pacotes

     ```sh
     poetry install
     ```

  5. Iniciar o servidor de desenvolvimento

     ```sh
     uvicorn musicop.app:app --reload
     ```

- Aqui caso estaja usando docker:

  3. Buildar pacote

     ```sh
     docker-compose up --build
     ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->

## Licença

Distribuido sobre MIT License. Veja `LICENSE.txt` para mais informações

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Felipe Maia - [@f.maia02](https://www.instagram.com/f.maia02/) - felipeoliveiramaia3@gmail.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/felipemaia02/musicoop)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

- [Choose an Open Source License](https://choosealicense.com)
- [README.md template](https://github.com/othneildrew/Best-README-Template)
- [Python](https://www.python.org/)
- [Postgres](https://www.postgresql.org/)
- [FastAPI](https://fastapi.tiangolo.com/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/felipemaia02/musicoop.svg?style=for-the-badge
[contributors-url]: https://github.com/felipemaia02/musicoop/contributors
[license-shield]: https://img.shields.io/github/license/felipemaia02/musicoop.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/felipeoliveira-maia/
