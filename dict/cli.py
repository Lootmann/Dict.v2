# src/cli.py
class CLI:
    @staticmethod
    def title(msg: str):
        print(f">>> {msg}")

    @staticmethod
    def print(cached_json: dict):
        """
        print cached json prettier
        """
        if "NotFound" in cached_json:
            print("This word is Not Found :^)")
            return

        print("[見出し語]", cached_json["headword"])

        if cached_json["description"] != "":
            print("[主な意味]", cached_json["description"])

        if "conjugation_table" in cached_json:
            max_pos_len = 0
            for part_of_speech in cached_json["conjugation_table"].keys():
                max_pos_len = max(max_pos_len, len(part_of_speech))

            # leading margin
            print()
            for pos, spell in cached_json["conjugation_table"].items():
                print("{}{}: {}".format("　" * (max_pos_len - len(pos)), pos, spell))

        print()

        for part_of_speech in [
            "動詞",
            "自動詞",
            "他動詞",
            "句動詞",
            "助動詞",
            "名詞",
            "可算名詞",
            "不可算名詞",
            "代名詞",
            "形容詞",
            "叙述的用法の形容詞",
            "限定用法の形容詞",
            "副詞",
            "前置詞",
            "接続詞",
            "間投詞",
            "冠詞",
        ]:
            if part_of_speech in cached_json:
                print(f"[{part_of_speech}]")
                for line in cached_json[part_of_speech]:
                    print("  ", line)

        # Examples
        for keyword in ["結果例文", "含む例文", "類似例文"]:
            if keyword in cached_json and len(cached_json[keyword]) > 0:
                print(f">>> {keyword}")
                for line in cached_json[keyword]:
                    print("  ", line)
            print()
