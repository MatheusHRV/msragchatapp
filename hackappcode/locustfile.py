import random
import time

from locust import HttpUser, between, task


class ChatUser(HttpUser):
    wait_time = between(5, 20)

    @task
    def ask_question(self):
        self.client.get("/")
        time.sleep(5)
        self.client.post(
            "/chat",
            json={
                "messages": [
                    {
                        "content": random.choice(
                            [
                                "Como fazer farófa de banana da terra?",
                                "Me mostre uma receita que possa ser feita em 30 minutos",
                                "Como fazer escondidinho de mandioca?",
                                "Sugira uma sobremesa com leite ninho",
                            ]
                        ),
                        "role": "user",
                    },
                ],
                "context": {
                    "overrides": {
                        "retrieval_mode": "hybrid",
                        "semantic_ranker": True,
                        "semantic_captions": False,
                        "top": 3,
                        "suggest_followup_questions": False,
                    },
                },
            },
        )
        time.sleep(5)
        self.client.post(
            "/chat",
            json={
                "messages": [
                    {"content": "Quais os ingredientes que preciso para fazer um bolinho de arroz?", "role": "user"},
                    {
                        "content": "1 xícara de arroz cozido, 1 unidade de ovo, ½ xícara de farinha de trigo ou de rosca, ½ xícara de queijo ralado, 1 unidade de cebola pequena, 1 copo pequeno de cheiro verde picado, 1 pitada de sal, 1 pitada de pimenta do reino, óleo para fritar",
                        "role": "assistant",
                    },
                    {"content": "Como fazer bolinho de chuva?", "role": "user"},
                ],
                "context": {
                    "overrides": {
                        "retrieval_mode": "hybrid",
                        "semantic_ranker": True,
                        "semantic_captions": False,
                        "top": 3,
                        "suggest_followup_questions": False,
                    },
                },
            },
        )
