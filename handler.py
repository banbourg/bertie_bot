import json
import os
import sys
import re
import random
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))

import requests

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)

emoji = {"wave": u"\U0001F44B", "purple_heart": u"\U0001F49C", "thumbs_up": u"\U0001F44D", "fire": u"\U0001F525"}


def hello(event, context):

    try:
        data = json.loads(event["body"])
        print(data)
        message = str(data["message"]["text"])
        chat_id = data["message"]["chat"]["id"]
        message_id = data["message"]["message_id"]
        first_name = str(data["message"]["from"]["first_name"])

        # Fetch bracketed name
        bn = re.search(r"\((.+)\)$", first_name)
        if bn:
            first_name = bn.group(1)

        # Remove emojis
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F953"  # iman's meat
                                   u"\U0001F356"
                                   u"\U0001F969"
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags=re.UNICODE)
        first_name = emoji_pattern.sub(r'', first_name)
        first_name = first_name[:-1] if first_name[-1] == " " else first_name

        print("first name:", first_name)

        # Check convo contents
        flag = 0
        msg = message.lower()
        drums = re.search(r"(?i)((?:stay|keep|kept|be|is|was|'s|'re|are).*in the loop)", msg)
        greeting = re.search(r"(?i)(h(?:ey|i[ ,.!?]|eya|ello).*bertie|bertie.*h(?:ey|i[!,. ?]|eya|ello))", msg)
        feelings = re.search(r"(?i)(?:i love (?:a )*(us|kat|tilda|tildis|kite|nina|evie|lae|maryam|gina|niamh|sam|taeri|becs|clara|yuzu|yuzuru|shoma|jason|satton))([\s.!,]|$)", msg)
        confession_1 = re.search(r"(?i)(bertie.+love you)", msg)
        confession_2 = re.search(r"(?i)(love (you)*.*bertie)", msg)
        confession_3 = re.search(r"(?i)(bertie.*love him)", msg)
        confession_4 = re.search(r"(?i)(bertie.+best|best.+bertie)", msg)
        #trello = re.search(r"(?i)(check.*trello)", msg)
        epithet = re.search(r"(?i)(?:bertie)(?:.*)(?: you)(?:'re | are )(.*)", msg)
        bertie = re.search(r"(?i)^(bert[i]+[e]+[!.]*)$", msg)
        terminator = re.search(r"(?i)(bert[i]+[e]+.*back|back.*bert[i]+[e]+)", msg)
        question_1 = re.search(r"(?i)you.+bert[i]+[e].*\?$", msg)
        question_2 = re.search(r"(?i)bert[i]+[e].+you.*\?$", msg)
        pls = re.search(r"(?i)bert[i]+[e]+ pl(ea)*s", msg)
        ci = re.search(r"Ci([\s.!,]|$)", message)
        wildciats = re.search(r"(?i)(what .*team(?:[\s?.!,]|$))", msg)
        faith = re.search(r"(believe|have faith) in you (\w+)", msg)

        b_r, dr_r, gr_r, te_r, p_r, despacito_r, despacito_r2, seimei_r = None, None, None, None, None, None, None, None
        c_r, e_r, fe_r, t_r, q_r, ci_r, wildciats_r, wildciats_r2 = None, None, None, None, None, None, None, None
        sectionals_r, faith_r = None, None
        if drums:
            dr_r = "BAH DUM TSSSSSSS "
        if greeting:
            gr_r = "Hello to you too " + first_name + " " + emoji["wave"] + "!! "
        if confession_1 or confession_2 or confession_3 or confession_4:
            c_r = "Aw shucks " + first_name + " I love you too " + emoji["purple_heart"] + emoji["purple_heart"] + "! "
        elif feelings:
            if re.search(r"(?i)(i love us)", msg):
                fe_r = "BERTIE LOVES AND SUPPORTS EVERYONE IN THIS HERE TEAM"
            else:
                fe_r = "I also love " + feelings.group(1) + " ; - ;"
        # if trello:
        #     t_r = "Make Tildis and Yogeeta proud, everyone! Always be checking Trello! " + emoji["thumbs_up"]
        if epithet and "back" not in epithet.group(1):
            e_r = "Well, I think you're " + epithet.group(1) + " too " + first_name + ", so there "
        if bertie:
            b_r = first_name + first_name[-1] + first_name[-1] + first_name[-1] + first_name[-1] + " :D"
        if terminator:
            te_r = "Did you miss me? :D "
        if question_1 or question_2:
            q_r = "I love how you're asking me questions like I'm sentient, no really I'm flattered "
        if pls and not all(item in msg for item in ["play", "despacito"]):
            p_r = "wat."
        if all(item in msg for item in ["bertie", "play", "despacito"]):
            despacito_r = "https://www.youtube.com/watch?v=kJQP7kiw5Fk"
        elif all(item in msg for item in ["play", "despacito"]):
            despacito_r2 = "uh my name is BERTIE but here: https://www.youtube.com/watch?v=kJQP7kiw5Fk "
        elif all(item in msg for item in ["play", "seimei"]):
            seimei_r = "GET LIT " + emoji["fire"] + emoji["fire"] + emoji["fire"] \
                       + " https://www.youtube.com/watch?v=23EfsN7vEOA "
        if ci:
            ci_r = "Ci "
        if wildciats:
            wildciats_r = "WILDCiATS"
        if "sectionals" in msg:
            sectionals_r = "SECTIONALLLLLLSSSSSSSSS"
        if faith:
            faith_r = "I also " + faith.group(1) + " in you " + faith.group(2)

        full_list = [ci_r, wildciats_r, sectionals_r, te_r, b_r, dr_r, gr_r, c_r, q_r, e_r, fe_r, p_r, despacito_r, despacito_r2,
                     seimei_r, faith_r]
        pop_list = [_f for _f in full_list if _f]
        if pop_list and random.random() < 20:
            response = " ".join(pop_list)
            data = {"text": response.encode("utf8"), "chat_id": chat_id, "reply_to_message_id": message_id}
            url = BASE_URL + "/sendMessage"

            requests.post(url, data)

    except Exception as e:
        print("Error: failed on ({})".format(e))

    return {"statusCode": 200}
