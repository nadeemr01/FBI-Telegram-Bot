import requests
import json
import pandas as pd


#------------------------------------------------------------------------------------------------------------------------------

all_items = []
page = 1
page_size = 50 
max_pages = 100   

while page <= max_pages:
    url = f"https://api.fbi.gov/wanted/v1/list?page={page}&pageSize={page_size}"
    response = requests.get(url)
    data = response.json()

    items = data.get("items", [])
    if not items:
        break

    all_items.extend(items)
    page += 1

df_main = pd.DataFrame(all_items)

#------------------------------------------------------------------------------------------------------------------------------
def Cyber_classification():
    df_main['subjects'] = df_main['subjects'].apply(lambda x: x if isinstance(x, list) else [x])
    df_cyber = df_main[df_main['subjects'].apply(lambda lst: "Cyber's Most Wanted" in lst)]
    df_cyber = df_cyber.dropna(subset=['nationality'])
    cyber_counts = df_cyber['nationality'].value_counts().head(5)
    msg = ["💻 Топ-5 самых разыскиваемых киберпреступников по национальности:"]
    for nat, num in cyber_counts.items():
        msg.append(f"{nat}: {num}")
    return "\n".join(msg)
#------------------------------------------------------------------------------------------------------------------------------
def Murders_classification():
    df_main['subjects'] = df_main['subjects'].apply(lambda x: x if isinstance(x, list) else [x])
    df_cyber = df_main[df_main['subjects'].apply(lambda lst: "Violent Crime - Murders" in lst)]
    df_cyber = df_cyber.dropna(subset=['nationality'])
    cyber_counts = df_cyber['nationality'].value_counts().head(5)
    msg = ["🔴 Топ-5 самых разыскиваемых насильственных преступлеников - убистц по национальности:"]
    for nat, num in cyber_counts.items():
        msg.append(f"{nat}: {num}")
    return "\n".join(msg)
#------------------------------------------------------------------------------------------------------------------------------
def Enterprise_classification():
    df_main['subjects'] = df_main['subjects'].apply(lambda x: x if isinstance(x, list) else [x])
    df_cyber = df_main[df_main['subjects'].apply(lambda lst: "Criminal Enterprise Investigations" in lst)]
    df_cyber = df_cyber.dropna(subset=['nationality'])
    cyber_counts = df_cyber['nationality'].value_counts().head(5)
    msg = ["🕵️ Топ-5 самых разыскиваемых по расследованию преступных организаций по национальности:"]
    for nat, num in cyber_counts.items():
        msg.append(f"{nat}: {num}")
    return "\n".join(msg)
#------------------------------------------------------------------------------------------------------------------------------
def Counterintelligence_classification():
    df_main['subjects'] = df_main['subjects'].apply(lambda x: x if isinstance(x, list) else [x])
    df_cyber = df_main[df_main['subjects'].apply(lambda lst: "Counterintelligence" in lst)]
    df_cyber = df_cyber.dropna(subset=['nationality'])
    cyber_counts = df_cyber['nationality'].value_counts().head(5)
    msg = ["🛡 Топ-5 самых разыскиваемых по контрразведка по национальности:"]
    for nat, num in cyber_counts.items():
        msg.append(f"{nat}: {num}")
    return "\n".join(msg)
#------------------------------------------------------------------------------------------------------------------------------
# analysis based on gender
def gender_based():
    df_sex = df_main.dropna(subset=["sex"])

    male_num = (df_sex["sex"] == "Male").sum()
    female_num = (df_sex["sex"] == "Female").sum()

    total = male_num + female_num

    male_percentage = male_num / total * 100
    female_percentage = female_num / total * 100

    return f"Мужчин в розыске: {male_num} ({male_percentage:.2f}%)\n" + f"Женшин в розыске: {female_num} ({female_percentage:.2f}%)"

#---------------------------------------------------------------
# analysis based on race
def race_based():
    df_race = df_main.dropna(subset=["race"])
    
    white_num = (df_race["race"] == "white").sum()
    black_num = (df_race["race"] == "black").sum()
    hispanic_num = (df_race["race"] == "hispanic").sum()
    asian_num = (df_race["race"] == "asian").sum()

    total_race = white_num + black_num + hispanic_num + asian_num

    white_percentage = white_num / total_race * 100
    black_percentage = black_num / total_race * 100
    hispanic_percentage = hispanic_num / total_race * 100
    asian_percentage = asian_num / total_race * 100

    return ( f"Белых в розыске: {white_num} ({white_percentage:.2f}%)\n" +
            f"Черных в розыске: {black_num} ({black_percentage:.2f}%)\n" + 
            f"латиноамериканев в розыске: {hispanic_num} ({hispanic_percentage:.2f}%)\n" + 
            f"Азиат в розыске: {asian_num} ({asian_percentage:.2f}%)"
            )

#------------------------------------------------------------------------------------------------------------------------------
# analysis based on nationality
def nationality_based():
    df_nationality = df_main.dropna(subset=["race"])
    
    ameriacn_num = (df_nationality["nationality"] == "American").sum()
    iranian_num = (df_nationality["nationality"] == "Iranian").sum()
    russian_num = (df_nationality["nationality"] == "Russian").sum()
    mexican_num = (df_nationality["nationality"] == "Mexican").sum()
    chinese_num = (df_nationality["nationality"] == "Chinese").sum()

    total_race = ameriacn_num + iranian_num + russian_num + mexican_num + chinese_num

    ameriacn_percentage = ameriacn_num / total_race * 100
    iranian_percentage = iranian_num / total_race * 100
    russian_percentage = russian_num / total_race * 100
    mexican_percentage = mexican_num / total_race * 100
    chinese_percentage = chinese_num / total_race * 100

    return ( f"Американцев в розыске: {ameriacn_num} ({ameriacn_percentage:.2f}%)\n" +
            f"Иранцев в розыске: {iranian_num} ({iranian_percentage:.2f}%)\n" + 
            f"Россян в розыске: {russian_num} ({russian_percentage:.2f}%)\n" + 
            f"Мексиканцев в розыске: {mexican_num} ({mexican_percentage:.2f}%)\n" +
            f"Китайцев в розыске: {chinese_num} ({chinese_percentage:.2f}%)"
            )

#------------------------------------------------------------------------------------------------------------------------------