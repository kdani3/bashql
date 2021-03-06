from pyparsing import Keyword, Regex, StringEnd, ZeroOrMore
from . import tree


kw_SELECT = Keyword("SELECT")
kw_DISTINCT = Keyword("DISTINCT")
kw_FROM = Keyword("FROM")
kw_STAR = Keyword("*")
kw_UNION = Keyword("UNION")
re_filename = Regex("[A-z\.0-9]+")
re_col_id = Regex("#[1-9][0-9]*")
file_list = ZeroOrMore(re_filename + kw_UNION) + re_filename
projection_star = kw_STAR
projection_columns = ZeroOrMore(re_col_id + ",") + re_col_id
projection = projection_star | projection_columns  # noqa
query_select = kw_SELECT + projection + kw_FROM + file_list
query_select_distinct = kw_SELECT + kw_DISTINCT + projection + kw_FROM + file_list  # noqa
query = (query_select + StringEnd()) | (query_select_distinct + StringEnd())


file_list.setParseAction(tree.FileList)
query_select.setParseAction(tree.SimpleSelect)
query_select_distinct.setParseAction(tree.SimpleSelectDistinct)
query.setParseAction(tree.Query)
projection_star.setParseAction(tree.ProjectionStar)
projection_columns.setParseAction(tree.ProjectionColumns)
projection.setParseAction(tree.passthrough)
