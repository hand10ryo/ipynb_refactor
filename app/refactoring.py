import openai

def refactor_and_document(py_file_path, api_key):
    with open(py_file_path, 'r') as f:
        code = f.read()

    openai.api_key = api_key

    txt = """
    以下はjupyter notebookのipynbファイルを.pyにコンバートしたファイルの内容です。
    入力されたコードをpepの基準に則ってリファクタリングしてください。
    特に、コードの整形、変数名・関数名の変更、コメントの追加、関数の分割などを行ってください。
    また、関数やクラス・メソッドにはdosctringも書いてください。
    そして最後に、セルに分割すべき部分に "\n[newline]\n" の文字列を挿入して適度に可読性を高めてください。
    """
    messages = [{"role": "user", "content":f"{txt} \n\n {code}"}]
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0,
    )
    refactored_code = response['choices'][0]['message']["content"]

    with open(py_file_path, 'w') as f:
        f.write(refactored_code)

    return py_file_path
