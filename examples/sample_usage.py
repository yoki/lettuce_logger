from lettuce_logger import pp, show_pp, get_logger, hide_pp  # noqa: F401


df = {
    "a": [1, 2, 3],
    "b": [4, 5, 6],
    "c": [7, 8, 9],
}

pp("hello")
hide_pp()
pp("dont show me")
show_pp()
pp("show me")
pp(get_logger)
pp(df)


mylog = get_logger("mylog")
pp("hello")
hide_pp()
pp("dont show me")
show_pp()
pp("show me")
