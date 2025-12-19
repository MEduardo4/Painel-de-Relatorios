def format_number(value, currency=False, decimals=0):
    """
    Formata números para exibição no padrão brasileiro (invertendo ponto e vírgula).
    Exemplo: 1234.56 vira '1.234,56'
    """
    # 1. Formata usando o padrão americano (vírgula separa milhar, ponto separa decimal)
    fmt = f"{{value:,.{decimals}f}}"
    
    # Adiciona R$ se for moeda
    if currency:
        fmt = "R$ " + fmt.format(value=value)
    else:
        fmt = fmt.format(value=value)

    # 2. Truque para inverter ponto e vírgula:
    # Troca vírgula por um texto temporário (_TEMP_)
    # Troca ponto por vírgula
    # Troca o texto temporário por ponto
    return fmt.replace(",", "_TEMP_").replace(".", ",").replace("_TEMP_", ".")
