# кубик
"""
парсит сообщения по маске
При наличии ключевых слов генерирует случайное число
опционально позволяет бросить кубик с нестандартным количеством граней
"""
import random
import re


class Dice:
    roll_pattern = r'(?i)^(?:roll|кубик|бросок(?: на)?) ?(\d{0,3}) (\.*)'  # FIXME change \. to \X
    faces = 20  # количество граней у кубика

    def check_roll(self, text: str):
        search = re.match(self.roll_pattern, text)
        if search:
            return True
        else:
            return False

    def roll(self, text: str):
        search = re.match(self.roll_pattern, text)
        if search:
            if search.group(1) and int(search.group(1)) > 1:
                dice = int(search.group(1))
            else: dice = self.faces
            clear_text = str(search.group(2))
            if dice > 2:
                val = random.randint(1, dice)
                string = str(clear_text + '\nШанс успеха: ' + '*' + str(val) + ' из ' + str(dice) + '*')
            else:
                val = random.choices(
                    population=['Успех', 'Неудача', 'Критический успех', 'Критическая неудача'],
                    weights=[0.45, 0.45, 0.05, 0.05],
                    k=1
                )
                string = str(clear_text + '\n' + '*' + str(*val) + '*')
            return string

    @staticmethod
    def drop(faces=faces):
        return random.randint(1, faces)


DICE_FACES = 20
reg_pattern = r'(?i)^(?:roll|кубик|бросок на) ?(\d{0,2}) (.*)'
test_text = 'кубик Some Random text?.. with some Char35act/#5er'

dice = Dice()
if __name__ == '__main__':
    print(dice.roll(test_text))
