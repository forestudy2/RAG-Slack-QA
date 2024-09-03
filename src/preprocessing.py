import os
import re
import shutil

# 원본 Notion 폴더 경로
folder_path = "src/origin_data"

# 정리된 파일 및 폴더를 저장할 data 폴더 경로
new_folder_path = "src/data"

# 특정 패턴의 폴더 이름을 검출하는 정규 표현식 (공백 포함한 32글자 및 16진수 패턴)
pattern = re.compile(r"\s*[a-f0-9]{32}\s*")


def clean_and_copy(src_path, dst_path):
    # 새로운 디렉토리 생성
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)

    # 현재 폴더의 하위 폴더와 파일 탐색
    for item in os.listdir(src_path):
        item_src_path = os.path.join(src_path, item)

        # 폴더 및 파일 이름에서 불필요한 패턴 제거
        cleaned_name = re.sub(pattern, "", item).strip()
        item_dst_path = os.path.join(dst_path, cleaned_name)

        if os.path.isdir(item_src_path):
            # 폴더인 경우 재귀적으로 처리
            clean_and_copy(item_src_path, item_dst_path)
            # 폴더 내용 복사 후 원본 폴더 삭제
            if not os.listdir(item_src_path):
                os.rmdir(item_src_path)
        else:
            # 파일인 경우 새로운 위치로 복사
            shutil.copy2(item_src_path, item_dst_path)

    # 빈 폴더 제거
    if not os.listdir(src_path) and src_path != new_folder_path:
        os.rmdir(src_path)


# 최상위 폴더에서 시작하여 모든 하위 폴더 및 파일 처리
clean_and_copy(folder_path, new_folder_path)

# 원본 폴더 삭제
if os.path.exists(folder_path):
    shutil.rmtree(folder_path)

print(
    "모든 폴더 및 파일 이름이 정리되어 'data'에 저장되었습니다. 원본 폴더는 삭제되었습니다."
)
