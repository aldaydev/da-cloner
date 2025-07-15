def detect_roles_from_files(file_paths, personaje):
    resultados = {}

    for file_path in file_paths:
        print(f"\n🔍 Analizando archivo: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"❌ Error al leer {file_path}: {e}")
            continue

        # Aplanar estructura
        bloques = []
        if isinstance(data, dict) and "speakers" in data:
            for speaker_data in data["speakers"]:
                speaker_name = speaker_data.get("speaker", "Unknown")
                for segment in speaker_data.get("segments", []):
                    bloques.append({
                        "speaker": speaker_name,
                        "text": segment.get("text", "")
                    })
        else:
            print(f"❌ Formato inválido en archivo: {file_path}")
            continue

        speakers = get_speakers(bloques)
        if len(speakers) > 2:
            print(f"⚠️ Más de 2 hablantes detectados en {file_path}. Se omite.")
            resultados[file_path] = {
                "interviewer": None,
                "interviewee": None
            }
            continue

        name_variants = generar_variantes_de_nombre(personaje)

        more_words = get_more_words(bloques)
        more_questions = get_more_questions(bloques)
        interpellate = get_interpellate(bloques, name_variants)
        welcome_speaker = get_welcome_speaker(bloques)

        print("DEBUG:")
        print("MORE_WORDS =>", more_words)
        print("MORE_QUESTIONS =>", more_questions)
        print("INTERPELLATE =>", interpellate)
        print("WELCOME_SPEAKER =>", welcome_speaker)


        # Lógica de inferencia
        interviewer = None
        interviewee = None
        # Caso 1: los tres factores coinciden y es distinto de more_words
        if more_questions == interpellate and more_questions == welcome_speaker and more_words != more_questions:
            interviewer = more_questions
        else:
            # Caso 2: algún speaker coincide en al menos dos de los tres factores y es distinto de more_words
            candidates = [more_questions, interpellate, welcome_speaker]
            for s in speakers:
                if candidates.count(s) >= 2 and s != more_words:
                    interviewer = s
                    break
        if interviewer:
            interviewee = [s for s in speakers if s != interviewer][0]
        resultados[file_path] = {
            "interviewer": interviewer,
            "interviewee": interviewee
        }

        print(f"🎯 Resultado para {file_path}:")
        print(f"   🗣️ Entrevistador: {interviewer}")
        print(f"   🎤 Entrevistado: {interviewee}")

    return resultados
