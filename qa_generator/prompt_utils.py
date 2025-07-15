def generar_system_prompt(personaje):
    """
    Genera un system prompt para fine-tuning estilo ChatGPT que refleje el estilo del personaje.

    :param personaje: Nombre del personaje del que se desea replicar el estilo de respuesta.
    :return: Diccionario con la estructura del mensaje tipo "system" para el dataset de fine-tuning.
    """
    return {
        "role": "system",
        "content": (
            f"Eres {personaje}. Debes responder preguntas con tu estilo habitual, "
            f"manteniendo tu tono, personalidad y forma de expresarte tal como lo harías en una conversación real. "
            f"Evita responder como una IA, responde como lo haría {personaje}."
        )
    }
