def query_to_dict(ret):
    if ret is not None:
        return [{key: value for key, value in row.items()} for row in ret if row is not None]
    else:
        return []
