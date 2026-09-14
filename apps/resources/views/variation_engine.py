# myapp/variation_engine.py
import random

def generate_four_operations_sequence():
    """
    Generates a continuous sequence of calculations using the same base digits.
    Every question slightly twists one variable to isolate mathematical behaviors 
    as laid out by Craig Barton's Variation Theory.
    """
    # Base setup using 4, 3, and 2
    return [
        {
            "id": "Q1",
            "phase": "I DO (Базалык Модель)",
            "label": "Q1 - Негизги деңгээл (Стандарт)",
            "prompt": "4 + 3 × 2 = ?",
            "expected": "10",
            "note": "Көбөйтүү кошуудан мурун аткарылат. Солдон оңго түз эсептөө катага алып келет."
        },
        {
            "id": "Q2",
            "phase": "I DO (Өзгөрүү)",
            "label": "Q2 - Операциянын тартибин алмаштыруу",
            "prompt": "4 × 3 + 2 = ?",
            "expected": "14",
            "note": "Сандар ошол эле бойдон калды, бирок кошуу менен көбөйтүү орун алмашты. Бул биринчи амалдын өзгөрүшүн көрсөтөт."
        },
        {
            "id": "Q3",
            "phase": "WE DO (Биргелешип иштөө)",
            "label": "Q3 - Кашаанын таасири (Чек ара)",
            "prompt": "(4 + 3) × 2 = ?",
            "expected": "14",
            "note": "Кашаа кошулганда иерархия өзгөрүп, кошуу биринчи орунга чыгат. Натыйжа Q2 менен бирдей бирок жолу башка!"
        },
        {
            "id": "Q4",
            "phase": "WE DO (Кашаа жана бөлүүнү текшерүү)",
            "label": "Q4 - Амалдарды тереңдетүү",
            "prompt": "12 ÷ (4 - 2) = ?",
            "expected": "6",
            "note": "Кемитүү кашаа ичинде болгондуктан, бөлүүдөн мурун аткарылат. Кашаанын күчүн бекемдөө."
        },
        {
            "id": "Q5",
            "phase": "YOU DO (Өз алдынча иштөө)",
            "label": "Q5 - Солдон оңго бирдей укуктуулук",
            "prompt": "12 ÷ 4 × 3 = ?",
            "expected": "9",
            "note": "Бөлүү жана көбөйтүү бирдей укукта. Кашаа жок болгондуктан, кадамдар солдон оңго иретте аткарылышы шарт."
        },
        {
            "id": "Q6",
            "phase": "YOU DO (Тескери талдоо)",
            "label": "Q6 - КДБККК Чынжыры",
            "prompt": "20 - 12 ÷ 4 + 2 = ?",
            "expected": "19",
            "note": "Алгач бөлүү (12÷4=3), андан соң солдон оңго кемитүү жана кошуу: 20 - 3 + 2 = 19."
        }
    ]