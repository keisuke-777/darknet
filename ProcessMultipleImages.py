import os
import re
import shutil
import csv
import time
import platform


def Predict(train, result):
    # 既存のtrain.txtがあれば削除
    if os.path.exists(train):
        os.remove(train)

    img_file_path = "multiple_predict/data"
    # directにある画像のファイル名を取得し昇順でソート
    jpg_name_list = sorted(os.listdir(img_file_path))

    train_str = ""
    for jpg_name in jpg_name_list:
        # 画像以外を弾く
        if re.match(".*\.(jpg|png)", jpg_name):
            train_str += img_file_path + "/" + jpg_name + "\n"

    # train.txtを作成
    with open(train, mode="w") as f:
        f.write(train_str)

    # 画像リストを解析
    if platform.system() == "Windows":
        darknet = "darknet.exe "
    else:  # Linux系
        darknet = "./darknet "

    # ちゃんと同期処理になるらしい
    os.system(
        darknet
        + "detector test cfg/coco.data cfg/yolov4.cfg yolov4.weights -dont_show -ext_output < "
        + train
        + " > "
        + result
    )


def ConvertToCsv(result):
    # resultをcsvに変換
    with open(result, mode="r") as f:
        result_str = f.read()
        result_list = result_str.split("multiple_predict/data/")
        for result_index in range(1, len(result_list)):
            single_predict_data = result_list[result_index]
            line = single_predict_data.split("\n")

            # 0行目に記載された画像のファイル名からcsvのパス+ファイル名を作成
            pic_name_end_index = re.search("\.(jpg|png)", line[0]).end()
            file_name = (
                "multiple_predict/result/" + line[0][:pic_name_end_index] + ".csv"
            )

            # csvに出力
            with open(file_name, "w") as csv_file:
                writer = csv.writer(csv_file, lineterminator="\n")
                for line_index in range(1, len(line)):
                    # 最後3行 or 1行に記載されている文言を認識したらbreak
                    if line[line_index].find("Enter Image Path") != -1:
                        break

                    # タイトル側と座標側に分離して作業
                    title_and_coordinate = line[line_index].split("(")

                    # タイトル側の処理
                    title_and_probability = title_and_coordinate[0].split(":")
                    title = title_and_probability[0]
                    probability = title_and_probability[1][:-1].replace(" ", "")

                    # 座標側の処理
                    coordinate_list = re.split(" +", title_and_coordinate[1])
                    left_x = coordinate_list[1]
                    top_y = coordinate_list[3]
                    width = coordinate_list[5]
                    height = coordinate_list[7][:-1]

                    csv_list = [title, probability, left_x, top_y, width, height]
                    writer.writerow(csv_list)


def main():
    train = "multiple_predict/train.txt"
    result = "multiple_predict/result.txt"
    Predict(train, result)
    ConvertToCsv(result)


if __name__ == "__main__":
    print(time.strftime("%Y/%m/%d %H:%M", time.strptime(time.ctime())))

    main()

    print(time.strftime("%Y/%m/%d %H:%M", time.strptime(time.ctime())))

    # test1
    # train = "multiple_predict/train.txt"
    # result = "multiple_predict/result.txt"
    # Predict(train, result)

    # test2
    # train = "multiple_predict/train.txt"
    # result = "multiple_predict/result.txt"
    # ConvertToCsv(result)

