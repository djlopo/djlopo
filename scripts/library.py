#!/usr/bin/env python3
"""Biblioteca de partes fijas (oraciones que se repiten siempre).

Textos canónicos de dominio público. Los generadores pueden importar de aquí para
que el texto sea EXACTO y así la caché (tts_cache) reutilice el audio entre vídeos.
BR = marca de pausa de ElevenLabs.
"""
BR = '<break time="0.6s" />'

SENAL_CRUZ = ("Por la señal de la Santa Cruz, de nuestros enemigos líbranos, Señor, Dios nuestro. "
              "En el nombre del Padre, y del Hijo, y del Espíritu Santo. Amén.")

GLORIA = ("Gloria al Padre, y al Hijo, y al Espíritu Santo. " + BR +
          " Como era en el principio, ahora y siempre, por los siglos de los siglos. Amén.")

PADRENUESTRO = ("Padre nuestro, que estás en el cielo, santificado sea tu Nombre; venga a nosotros tu reino; "
                "hágase tu voluntad en la tierra como en el cielo. Danos hoy nuestro pan de cada día; "
                "perdona nuestras ofensas, como también nosotros perdonamos a los que nos ofenden; "
                "no nos dejes caer en la tentación, y líbranos del mal. Amén.")

# Padrenuestro partido para rezo a dos voces (guía / pueblo). El corte tradicional
# separa las tres peticiones "tuyas" (Nombre, reino, voluntad) de las peticiones "nuestras"
# (pan, perdón, tentación, mal).
PADRENUESTRO_1 = ("Padre nuestro, que estás en el cielo, santificado sea tu Nombre; venga a nosotros tu reino; "
                  "hágase tu voluntad en la tierra como en el cielo.")
PADRENUESTRO_2 = ("Danos hoy nuestro pan de cada día; perdona nuestras ofensas, como también nosotros perdonamos "
                  "a los que nos ofenden; no nos dejes caer en la tentación, y líbranos del mal. Amén.")

# Gloria partido para rezo a dos voces (guía / pueblo).
GLORIA_1 = "Gloria al Padre, y al Hijo, y al Espíritu Santo."
GLORIA_2 = "Como era en el principio, ahora y siempre, por los siglos de los siglos. Amén."

# Pasaje bíblico (Palabra de Dios) de cada misterio, para proclamarlo antes de meditarlo.
# Referencias del Leccionario; los textos se toman de la Biblia en cada generador.
MISTERIOS_GOZOSOS_BIBLIA = {
    1: "Lucas 1, 26-38",   # La Encarnación (Anunciación)
    2: "Lucas 1, 39-45",   # La Visitación
    3: "Lucas 2, 1-14",    # El Nacimiento de Jesús
    4: "Lucas 2, 22-35",   # La Presentación en el templo
    5: "Lucas 2, 41-52",   # El Niño perdido y hallado
}
MISTERIOS_DOLOROSOS_BIBLIA = {
    1: "Lucas 22, 39-46",  # Oración en el huerto
    2: "Marcos 15, 6-15",  # Flagelación
    3: "Marcos 15, 16-20", # Coronación de espinas
    4: "Lucas 23, 26-32",  # Camino del Calvario
    5: "Lucas 23, 33-46",  # Crucifixión y muerte
}
MISTERIOS_GLORIOSOS_BIBLIA = {
    1: "Marcos 16, 1-8",   # Resurrección
    2: "Lucas 24, 50-53",  # Ascensión
    3: "Hechos 2, 1-13",   # Venida del Espíritu Santo
    4: "Lucas 1, 46-55",   # Asunción de María
    5: "Apocalipsis 12, 1",  # Coronación de María
}
MISTERIOS_LUMINOSOS_BIBLIA = {
    1: "Mateo 3, 13-17",   # Bautismo en el Jordán
    2: "Juan 2, 1-11",     # Bodas de Caná
    3: "Marcos 1, 14-15",  # Anuncio del Reino
    4: "Lucas 9, 28-36",   # Transfiguración
    5: "Lucas 22, 14-20",  # Institución de la Eucaristía
}

# Avemaría partida para el dúo del Rosario (una voz / respuesta la otra)
AVEMARIA_1 = ("Dios te salve, María; llena eres de gracia; el Señor es contigo; "
              "bendita tú eres entre todas las mujeres, y bendito es el fruto de tu vientre, Jesús.")
AVEMARIA_2 = ("Santa María, Madre de Dios, ruega por nosotros, pecadores, "
              "ahora y en la hora de nuestra muerte. Amén.")

JACULATORIA_FATIMA = ("Oh Jesús mío, perdona nuestros pecados, líbranos del fuego del infierno, "
                      "lleva al cielo a todas las almas, especialmente a las más necesitadas de tu misericordia.")

SALVE = ("Dios te salve, Reina y Madre de misericordia, vida, dulzura y esperanza nuestra; Dios te salve. "
         "A ti llamamos los desterrados hijos de Eva; a ti suspiramos, gimiendo y llorando, en este valle de lágrimas. "
         "Ea, pues, Señora, abogada nuestra, vuelve a nosotros esos tus ojos misericordiosos; "
         "y después de este destierro muéstranos a Jesús, fruto bendito de tu vientre. "
         "¡Oh clementísima, oh piadosa, oh dulce Virgen María!")

# Respuestas del pueblo (Misa)
R_TE_ALABAMOS = "Te alabamos, Señor."
R_GLORIA_A_TI = "Gloria a ti, Señor Jesús."
R_AMEN = "Amén."
R_ALELUYA = "Aleluya, aleluya, aleluya."

# Cánticos evangélicos (fijos cada día)
BENEDICTUS = ("Bendito sea el Señor, Dios de Israel, porque ha visitado y redimido a su pueblo, "
              "suscitándonos una fuerza de salvación en la casa de David, su siervo, según lo había predicho "
              "desde antiguo por boca de sus santos profetas. " + BR +
              " Es la salvación que nos libra de nuestros enemigos y de la mano de todos los que nos odian; "
              "ha realizado así la misericordia que tuvo con nuestros padres, recordando su santa alianza "
              "y el juramento que juró a nuestro padre Abrahán. " + BR +
              " Para concedernos que, libres de temor, arrancados de la mano de los enemigos, le sirvamos "
              "con santidad y justicia, en su presencia, todos nuestros días. " + BR +
              " Y a ti, niño, te llamarán Profeta del Altísimo, porque irás delante del Señor a preparar sus caminos, "
              "anunciando a su pueblo la salvación, el perdón de sus pecados. " + BR +
              " Por la entrañable misericordia de nuestro Dios, nos visitará el sol que nace de lo alto, "
              "para iluminar a los que viven en tiniebla y en sombra de muerte, para guiar nuestros pasos "
              "por el camino de la paz. " + BR + " " + GLORIA)

MAGNIFICAT = ("Proclama mi alma la grandeza del Señor, se alegra mi espíritu en Dios, mi salvador; "
              "porque ha mirado la humildad de su esclava. " + BR +
              " Desde ahora me felicitarán todas las generaciones, porque el Poderoso ha hecho obras grandes por mí: "
              "su nombre es santo, y su misericordia llega a sus fieles de generación en generación. " + BR +
              " Él hace proezas con su brazo: dispersa a los soberbios de corazón, derriba del trono a los poderosos "
              "y enaltece a los humildes, a los hambrientos los colma de bienes y a los ricos los despide vacíos. " + BR +
              " Auxilia a Israel, su siervo, acordándose de la misericordia, como lo había prometido a nuestros padres, "
              "en favor de Abrahán y su descendencia por siempre. " + BR + " " + GLORIA)

# Misterios del Rosario por día de la semana (0=lunes)
MISTERIOS_POR_DIA = {
    0: "Gozosos", 1: "Dolorosos", 2: "Gloriosos", 3: "Luminosos",
    4: "Dolorosos", 5: "Gozosos", 6: "Gloriosos",
}
