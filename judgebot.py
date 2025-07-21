import json 
import sys

# Mot clé
keywords_guilty = [
    "vol", "falsifi", "fraude", "arme", "cambriol", "menace", "fuite", "triche", "détourne", "agressé", "ivre", "avoue",
    "complice", "chantage", "violence", "agression", "homicide", "meurtre", "incendie", "escroquerie", "abus de confiance",
    "délit", "coupable", "recel", "drogue", "trafic", "enlèvement", "menaces", "attaque", "sabotage"
]

keywords_not_guilty = [
    "alibi", "preuve disculpatoire", "erreur", "ressemblance", "factice", "insuffisance", "légitime défense", "sans preuve",
    "libérée", "relaxé", "insuffisantes", "erronée", "non-violent", "pacifique", "témoins",
    "innocent", "acquitté", "non prouvé", "absence de preuve", "témoignage favorable", "justifié", "non intentionnel",
    "accident", "malentendu", "confusion", "doute raisonnable", "non impliqué", "présomption d'innocence"
]

def find_similar_case(description, detected_keywords):
    """Trouve un cas similaire dans la base de données JSON"""
    try:
        with open("cases.json", mode='r', encoding='utf-8') as f:
            data = json.load(f)
        # chercher cas avec mêmes mots-clés
        for case in data:
            case_text = case['case'].lower()
            for keyword in detected_keywords:
                if keyword in case_text:
                    return case
        return data[0] if data else None
    except FileNotFoundError:
        return None


def predict_verdict(description):
    """Analyse une description et prédit le verdict"""
    text = description.lower()
    justification = []
    verdict = "NOT GUILTY"  
    detected_keywords = []
    # chercher mot d culpab
    for word in keywords_guilty:
        if word in text:
            verdict = "GUILTY"
            justification.append(f"mot-clé de culpabilité détecté : '{word}'.")
            detected_keywords.append(word)
    # chercher mot d pas culpab
    for word in keywords_not_guilty:
        if word in text:
            verdict = "NOT GUILTY"
            justification.append(f"mot-clé disculpant détecté : '{word}'.")
            detected_keywords.append(word)
    if not justification:
        justification = ["aucun mot-clé détecté. décision par défaut : NOT GUILTY."]
    return verdict, " ".join(justification), detected_keywords



def process_json_file(filename):
    """pass sur fichier JSON"""
    with open(filename, mode='r', encoding='utf-8') as f:
        data = json.load(f)
    for case in data:
        case_id = case['id']
        description = case['description']
        predicted_verdict, justification, _ = predict_verdict(description)

        print(f"cas #{case_id}")
        print(f"description : {description}")
        print(f"verdict prédit : {predicted_verdict}")
        print(f"justification : {justification}")
        print("-" * 60)


def main():
    if len(sys.argv) == 2:
        # analyse cas utilisateur
        user_input = sys.argv[1]
        verdict, explanation, detected_keywords = predict_verdict(user_input)
        
        # resemblance
        similar_case = find_similar_case(user_input, detected_keywords)
        
        if similar_case:
            print(f"description : {similar_case['description']}")
            print(f"cas similaire trouvé (#{similar_case['id']}) : {similar_case['case']}")
        else:
            print(f"description : {user_input}")
            print("aucun cas similaire trouvé dans la base de données.")
            
        print(f"verdict : {verdict}")
        print(f"justification : {explanation}")
    else:
        process_json_file("cases.json")

if __name__ == "__main__":
    main()