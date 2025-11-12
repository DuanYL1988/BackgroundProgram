import argparse

USERNAMED = ""
PASSWORD = ""
FILENAMES = []

def main():
    print(f"{USERNAMED},{PASSWORD},{FILENAMES[0]}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="命令行参数示例")
    parser.add_argument("-u", "--username", default="admin", help="ユーザーネーム")
    parser.add_argument("-p", "--password", default="123456", help="パスワード")
    parser.add_argument("-f", "--files", default=[], help="ファイル")
    arges = parser.parse_args()
    USERNAMED = arges.username
    PASSWORD = arges.password
    FILENAMES = arges.files.split(",")
    main()

