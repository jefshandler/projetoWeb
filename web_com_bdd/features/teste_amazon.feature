Feature: Adicionar produto ao carrinho na Amazon
  Scenario Outline: Pesquisar um produto na Amazon e adicioná-lo ao carrinho
    Given que eu acesse a página da Amazon e comparamos o titulo
    When eu pesquisar por um produto "<termo_pesquisa>"
    Then o produto pesquisado deve ser exibido na página de resultados "<produto_pesquisado>"
    When eu seleciono o produto pesquisado "<produto_pesquisado>"
    Then o produto e preço, do produto  selecionado deve estar correto "<produto_pesquisado>", "<valor_produto>"
    When eu adicionar o produto ao carrinho
    Then a mensagem de sucesso deve ser exibida "<mensagem_de_sucesso>"
    When eu acessar o carrinho
    Then o produto adicionado deve estar no carrinho "<produto_pesquisado>"
    Then o preço do produto no carrinho deve estar correto "<valor_carrinho>"
    And eu fecho o navegador

    Examples:
      |termo_pesquisa|produto_pesquisado|valor_produto|mensagem_de_sucesso|valor_carrinho|
      |HD Portatil Externo 1TB|HD Externo 1TB USB 3.0 Seagate Expansion Portátil (STEA1000400)|336|Adicionado ao carrinho|R$ 336,90|

    # pode usar o terminal e executar o comando (behave features\teste_amazon.feature)