a = 0
# [SAMPLE]
b = 1
c = 2
# [SAMPLE]
def test_func(arg1=None, arg2=None):
    """desc
    `Sphinx reStructuretext docs <https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html>`_
    *emphasis* and **more emphasis**

    :param str arg1: AAA see class :py:class:`tests.test_docs.DummyClass`
    :param arg2: BBB ``True``, see :ref:`codeblock`
    :type arg2: dict{str, int}, see :py:func:`tests.test_docs.test_func`
    :return: None
    :rtype: None or str
    :raise ValueError: raises ValueError exception.

    .. code-block:: Python
        :caption: code block title
        :name: codeblock
        :linenos:
        :emphasize-lines: 1,4

        test_docs(111, 222)
        a = 1
        b = 2
        return
    
    .. note::
        this is note
    .. warning::
        this is a warning
    .. versionadded:: 1.1
        add by 1.1
    .. versionchanged:: 1.2
        change 1.2
    .. deprecated:: 1.3
        deprecated

    Include code section

    .. literalinclude:: /../../tests/test_docs.py
        :language: python
        :start-after: [SAMPLE]
        :end-before: [SAMPLE]

    Include code function

    .. literalinclude:: /../../tests/test_docs.py
        :language: python
        :pyobject: test_func
    """

class DummyClass:
    """DummyClass
    """
    pass

def priv_func():
    """private function should not show in docs

    :meta private:
    """
    



