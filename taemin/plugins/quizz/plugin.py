# -*- coding: utf8 -*-

from collections import defaultdict
import glob
import os
import random

from taemin import plugin

class TaeminQuizz(plugin.TaeminPlugin):
    helper = {"quizz": "taemin quizz. Usage !quizz nom_du_quizz [reponse]"}

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    QUIZZ_LOCATIONS = os.path.join(__location__, "quizzs")

    def __init__(self, taemin):
        plugin.TaeminPlugin.__init__(self, taemin)
        self.quizzs = self._load_quizz()

        self.ongoing_quizzs = defaultdict(list)
        self.current_questions = {}

    def on_pubmsg(self, msg):
        if msg.key not in self.helper:
            return

        chan = msg.chan.name

        if not msg.value.strip():
            self.privmsg(chan, self.helper[msg.key])
            return

        pvalue = msg.value.split(" ", 1)
        quizz = pvalue[0]
        if quizz not in self.quizzs:
            self.privmsg(chan, "Quizz invalide, quizz disponible: %s" % list(self.quizzs.keys()))
            return

        if not self.current_question(quizz):
            self.restart_quizz(quizz)

        if len(pvalue) == 1:
            self.privmsg(
                chan,
                "Question: %s" % self.current_question(quizz)[0]
            )
            return

        answer = pvalue[1]

        valid_answer = self.current_question(quizz)[1]
        if self.answer_quizz(quizz, answer):
            self.privmsg(
                chan,
                "Bonne réponse! question suivante: %s" % (
                    self.current_question(quizz)[0]
                )
            )
        else:
            self.privmsg(chan, "Mauvaise réponse! c'était %s. Nouvelle question: %s" % (
                valid_answer,
                self.current_question(quizz)[0]
            ))

    @classmethod
    def _load_quizz(cls):
        quizzs = {}
        for file_name in glob.glob("%s/*.csv" % cls.QUIZZ_LOCATIONS):
            with open(file_name, 'r', encoding="utf-8") as f:
                name = os.path.basename(file_name).rsplit(".", 1)[0]
                quizzs[name] = []
                for line in f.readlines():
                    quizzs[name].append(line.replace("\n", "").split(",", 1))
        return quizzs

    def get_new_question(self, quizz):
        """ Get a random new question for a given quizz """

        available_questions = [
            question for question in self.quizzs[quizz]
            if question not in self.ongoing_quizzs[quizz]
        ]
        if not available_questions:
            return None

        return random.choice(available_questions)

    def current_question(self, quizz):
        """ Return the current question for a given quizz """

        if self.current_questions.get(quizz):
            return self.current_questions[quizz]

        self.current_questions[quizz] = self.get_new_question(quizz)
        return self.current_questions[quizz]

    def answer_quizz(self, quizz, answer, reverse=False):
        """ test to answer to a question """

        if not self.current_question(quizz):
            return False

        res = answer.lower() == self.current_question(quizz)[int(not reverse)].lower()
        if res:
            self.ongoing_quizzs[quizz].append(self.current_question(quizz))
            self.current_questions.pop(quizz, None)
        else:
            self.restart_quizz(quizz)

        return res

    def restart_quizz(self, quizz):
        """ Restart a given quizz """

        self.ongoing_quizzs[quizz] = []
        self.current_questions.pop(quizz, None)

if __name__ == "__main__":
    print(TaeminQuizz(None).quizzs)

    print(TaeminQuizz(None).current_question("capitales"))
