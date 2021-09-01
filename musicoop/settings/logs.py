"""
Módulo responsável pela configuração e formatação do Logger da aplicação
"""
import logging

logging.basicConfig(
    format=('%(asctime)s,%(msecs)-3d - %(name)-12s - %(levelname)-8s => '
            '%(message)s'),
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)
