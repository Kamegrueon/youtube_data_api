def extract_datetime_from_file_path(file_path: str) -> str:
    split_str = file_path.split("/")[1]
    date = f"{split_str[0:4]}-{split_str[4:6]}-{split_str[6:8]}"
    time = f"{split_str[8:10]}:{split_str[10:12]}:00"
    return f"{date} {time}"
