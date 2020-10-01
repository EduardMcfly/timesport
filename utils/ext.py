from typing import Any
from jinja2.ext import Extension
from jinja2 import lexer, nodes
from flask import url_for
from abc import abstractmethod, abstractproperty


class JinjaBase(Extension):
    @abstractproperty
    def tags(self):
        pass

    @abstractmethod
    def getValue(self, value: Any):
        pass

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        token = parser.stream.expect(lexer.TOKEN_STRING)
        value = nodes.Const(token.value)
        call = self.call_method('getValue', [value], lineno=lineno)
        token = parser.stream.current
        if token.test('name:as'):
            next(parser.stream)
            as_var = parser.stream.expect(lexer.TOKEN_NAME)
            as_var = nodes.Name(as_var.value, 'store', lineno=as_var.lineno)
            return nodes.Assign(as_var, call, lineno=lineno)
        else:
            return nodes.Output([call], lineno=lineno)


class JinjaStatic(JinjaBase):
    tags = {"static"}

    def getValue(self, path):
        return url_for('static', filename=path)
