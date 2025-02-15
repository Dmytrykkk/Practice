from sentence_transformers import SentenceTransformer, util

# Завантажуємо багатомовну модель
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

def compare_texts(text1, text2):
    # Отримуємо векторні представлення текстів
    embedding1 = model.encode(text1, convert_to_tensor=True)
    embedding2 = model.encode(text2, convert_to_tensor=True)

    # Обчислюємо косинусну схожість
    similarity = util.pytorch_cos_sim(embedding1, embedding2).item()

    return similarity  # Повертаємо значення від 0 до 1 (чим ближче до 1, тим схожіші тексти)

"""# Приклад 
text1 = "The European Union will review its multi-billion-dollar foreign aid — they want the distribution of funds to be more in line with the blocʼs foreign policy interests in the difficult international situation.This is reported by Bloomberg with reference to the draft of the relevant document.The publication notes that this is happening at a time when the number of priorities, including defense due to the war in Ukraine, is increasing, and the new US President Donald Trump is hostile.Read more:Trump threatens to impose tariffs on EU countries — European leaders reactThe European Commission wants to deliver foreign aid on better terms, modernising it and making it more useful for partners. It will outline ideas for improving its next seven-year budget from 2028 to 2034 in the coming weeks.The bloc wants to restructure foreign aid to ensure its strategic interests, including strengthening alliances with like-minded countries, access to raw materials, and curbing the influx of migrants.The document, seen by Bloomberg, notes that the blocʼs overall budget, which amounts to about 1% of EU GDP, is overstretched due to a wide range of spending — from the green transition information referenceThis is a process of gradual transition to an environmentally friendly economy that uses less fossil fuels (oil, gas, coal) and more renewable energy sources (sun, wind, water).to defense.Bloomberg writes that the European Commissionʼs plan coincides with Trumpʼs decision to eliminate the United States Agency for International Development (USAID), which allocates tens of billions of dollars in aid each year"
text2 = "Європейський Союз перегляне багатомільярдну зовнішню допомогу, щоб більше узгодити розподіл коштів з зовнішньополітичними інтересами блоку.Про це пише Bloomberg.Зазначається, що Єврокомісія, виконавчий орган ЄС, хоче стати більш транзакційною, реформуючи зовнішню допомогу і роблячи її більш адресною для партнерів.Блок має на меті реструктуризувати зовнішню допомогу для забезпечення своїх стратегічних інтересів, включаючи зміцнення альянсів з країнами-однодумцями, забезпечення доступу до сировини та стримування припливу мігрантів.У проєкті документа, який ще може бути змінений до презентації, зазначається, що загальний бюджет ЄС, який традиційно становить близько 1% ВВП блоку, перенапружений з огляду на широкий спектр вимог - від зеленого переходу до оборони.У найближчі тижні комісія представить ідеї щодо поліпшення свого наступного семирічного бюджету на період з 2028 по 2034 рік.План комісії збігається з рішенням Трампа ліквідувати Агентство США з міжнародного розвитку (USAID), яке щороку розподіляє закордонну допомогу на десятки мільярдів доларів.ЄС та його держави-члени разом є найбільшим донором міжнародної допомоги у світі, надавши майже 96 мільярдів євро (99 мільярдів доларів) у 2023 році, тоді як США витратили майже 72 мільярди доларів на зовнішню підтримку.Читайте також: Які державні органи та організації не отримають кошти через призупинення фінансування USAID? СписокНагадаємо:Радник президента США Дональда Трампа з питань національної безпеки Майк Волц не вважає, що відмова від закордонної гуманітарної допомоги призведе до того, що Штати поступляться Китаю та Росії контролем на світовій арені.Адміністрація президента США Дональда Трампа оприлюднила перелік розтрат та зловживань в Агентстві США з міжнародного розвитку (USAID)."

similarity_score = compare_texts(text1, text2)
print(f"Схожість текстів: {similarity_score:.2f}")
"""