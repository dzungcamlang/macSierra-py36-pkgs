from os.path import abspath, dirname, join
import textwrap

import pytest

from ..table import Table
from ... import extern
from ...extern.six.moves import zip

try:
    import IPython  # pylint: disable=W0611
except ImportError:
    HAS_IPYTHON = False
else:
    HAS_IPYTHON = True

EXTERN_DIR = abspath(dirname(extern.__file__))

REFERENCE = """
<html>
 <head>
  <meta charset="utf-8"/>
  <meta content="text/html;charset=UTF-8" http-equiv="Content-type"/>
  <style>
body {font-family: sans-serif;}
table.dataTable {width: auto !important; margin: 0 !important;}
.dataTables_filter, .dataTables_paginate {float: left !important; margin-left:1em}
  </style>
  <link href="%(datatables_css_url)s" rel="stylesheet" type="text/css"/>
  <script src="%(jquery_url)s">
  </script>
  <script src="%(datatables_js_url)s">
  </script>
 </head>
 <body>
  <script>
var astropy_sort_num = function(a, b) {
    var a_num = parseFloat(a);
    var b_num = parseFloat(b);

    if (isNaN(a_num) && isNaN(b_num))
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    else if (!isNaN(a_num) && !isNaN(b_num))
        return ((a_num < b_num) ? -1 : ((a_num > b_num) ? 1 : 0));
    else
        return isNaN(a_num) ? -1 : 1;
}

jQuery.extend( jQuery.fn.dataTableExt.oSort, {
    "optionalnum-asc": astropy_sort_num,
    "optionalnum-desc": function (a,b) { return -astropy_sort_num(a, b); }
});

$(document).ready(function() {
    $('#%(table_id)s').dataTable({
        order: [],
        pageLength: %(length)s,
        lengthMenu: [[%(display_length)s, -1], [%(display_length)s, 'All']],
        pagingType: "full_numbers",
        columnDefs: [{targets: [0], type: "optionalnum"}]
    });
} );  </script>
  <table class="%(table_class)s" id="%(table_id)s">
   <thead>
    <tr>
     <th>a</th>
     <th>b</th>
    </tr>
   </thead>
%(lines)s
  </table>
 </body>
</html>
"""

TPL = ('   <tr>\n'
       '    <td>{0}</td>\n'
       '    <td>{1}</td>\n'
       '   </tr>')


def format_lines(col1, col2):
    return '\n'.join(TPL.format(a, b) for a, b in zip(col1, col2))


def test_write_jsviewer_default(tmpdir):
    t = Table()
    t['a'] = [1, 2, 3, 4, 5]
    t['b'] = ['a', 'b', 'c', 'd', 'e']
    t['a'].unit = 'm'

    tmpfile = tmpdir.join('test.html').strpath

    t.write(tmpfile, format='jsviewer')
    ref = REFERENCE % dict(
        lines=format_lines(t['a'], t['b']),
        table_class='display compact',
        table_id='table%s' % id(t),
        length='50',
        display_length='10, 25, 50, 100, 500, 1000',
        datatables_css_url='https://cdn.datatables.net/1.10.12/css/jquery.dataTables.css',
        datatables_js_url='https://cdn.datatables.net/1.10.12/js/jquery.dataTables.min.js',
        jquery_url='https://code.jquery.com/jquery-3.1.1.min.js'
    )
    with open(tmpfile) as f:
        assert f.read().strip() == ref.strip()


def test_write_jsviewer_options(tmpdir):
    t = Table()
    t['a'] = [1, 2, 3, 4, 5]
    t['b'] = ['a', 'b', 'c', 'd', 'e']
    t['a'].unit = 'm'

    tmpfile = tmpdir.join('test.html').strpath

    t.write(tmpfile, format='jsviewer', table_id='test', max_lines=3,
            jskwargs={'display_length': 5}, table_class='display hover')
    ref = REFERENCE % dict(
        lines=format_lines(t['a'][:3], t['b'][:3]),
        table_class='display hover',
        table_id='test',
        length='5',
        display_length='5, 10, 25, 50, 100, 500, 1000',
        datatables_css_url='https://cdn.datatables.net/1.10.12/css/jquery.dataTables.css',
        datatables_js_url='https://cdn.datatables.net/1.10.12/js/jquery.dataTables.min.js',
        jquery_url='https://code.jquery.com/jquery-3.1.1.min.js'
    )
    with open(tmpfile) as f:
        assert f.read().strip() == ref.strip()


def test_write_jsviewer_local(tmpdir):
    t = Table()
    t['a'] = [1, 2, 3, 4, 5]
    t['b'] = ['a', 'b', 'c', 'd', 'e']
    t['a'].unit = 'm'

    tmpfile = tmpdir.join('test.html').strpath

    t.write(tmpfile, format='jsviewer', table_id='test',
            jskwargs={'use_local_files': True})
    ref = REFERENCE % dict(
        lines=format_lines(t['a'], t['b']),
        table_class='display compact',
        table_id='test',
        length='50',
        display_length='10, 25, 50, 100, 500, 1000',
        datatables_css_url='file://' + join(EXTERN_DIR, 'css', 'jquery.dataTables.css'),
        datatables_js_url='file://' + join(EXTERN_DIR, 'js', 'jquery.dataTables.min.js'),
        jquery_url='file://' + join(EXTERN_DIR, 'js', 'jquery-3.1.1.min.js')
    )
    with open(tmpfile) as f:
        assert f.read().strip() == ref.strip()


@pytest.mark.skipif('not HAS_IPYTHON')
def test_show_in_notebook():
    t = Table()
    t['a'] = [1, 2, 3, 4, 5]
    t['b'] = ['b', 'c', 'a', 'd', 'e']

    htmlstr_windx = t.show_in_notebook().data  # should default to 'idx'
    htmlstr_windx_named = t.show_in_notebook(show_row_index='realidx').data
    htmlstr_woindx = t.show_in_notebook(show_row_index=False).data

    assert (textwrap.dedent("""
    <thead><tr><th>idx</th><th>a</th><th>b</th></tr></thead>
    <tr><td>0</td><td>1</td><td>b</td></tr>
    <tr><td>1</td><td>2</td><td>c</td></tr>
    <tr><td>2</td><td>3</td><td>a</td></tr>
    <tr><td>3</td><td>4</td><td>d</td></tr>
    <tr><td>4</td><td>5</td><td>e</td></tr>
    """).strip() in htmlstr_windx)

    assert '<thead><tr><th>realidx</th><th>a</th><th>b</th></tr></thead>' in htmlstr_windx_named

    assert '<thead><tr><th>a</th><th>b</th></tr></thead>' in htmlstr_woindx