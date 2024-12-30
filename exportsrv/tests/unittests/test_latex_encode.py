# -*- coding: utf-8 -*-

from flask_testing import TestCase
import unittest

import exportsrv.app as app

from exportsrv.formatter.latexencode import utf8tolatex


class TestLatexEncode(TestCase):

    def create_app(self):
        app_ = app.create_app()
        return app_


    def test_ascii_characters(self):
        text = u'  ! " # $ % \\ \' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ ' + \
               u'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \ ] ^ _ ` ' + \
               u'a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~'
        latex = "  ! '' \# \$ \% \\textbackslash " + \
                "' ( ) * + , - . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ " + \
                "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ \\textbackslash ] \\^ \\_ ` " + \
                "a b c d e f g h i j k l m n o p q r s t u v w x y z \\{ | \\} \\raisebox{-0.5ex}\\textasciitilde"
        assert (utf8tolatex(text, ascii_no_brackets=True) == latex)


    def test_latin1_supplement(self):
        text = u'¡ ¢ £ ¤ ¥ ¦ § ¨ © ª « ¬ ® ¯ ° ± ² ³ ´ µ ¶ · ¸ ¹ º » ¼ ½ ¾ ¿ ' + \
               u'À Á Â Ã Ä Å Æ Ç È É Ê Ë Ì Í Î Ï Ð Ñ Ò Ó Ô Õ Ö × Ø Ù Ú Û Ü Ý Þ ß ' + \
               u'à á â ã ä å æ ç è é ê ë ì í î ï ð ñ ò ó ô õ ö ÷ ø ù ú û ü ý þ ÿ'
        latex = u'{\\textexclamdown} {\\textcent} {\\textsterling} {\\textcurrency} {\\textyen} {\\textbrokenbar} ' + \
                u'{\\textsection} {\\textasciidieresis} {\\textcopyright} {\\textordfeminine} {\\guillemotleft} ' + \
                u'{\\textlnot} {\\textregistered} {\\textasciimacron} {\\textdegree} {\\ensuremath{\\pm}} ' + \
                u'{\\texttwosuperior} {\\textthreesuperior} {\\textasciiacute} {\\textmu} {\\textparagraph} ' + \
                u'{\\textperiodcentered} ¸ {\\textonesuperior} {\\textordmasculine} {\\guillemotright} {\\textonequarter} ' + \
                u'{\\textonehalf} {\\textthreequarters} {\\textquestiondown} ' + \
                u'{\\`A} {\\\'A} {\\^A} {\\~A} {\\"A} {\\r{A}} {\\AE} {\\c{C}} {\\`E} {\\\'E} {\\^E} {\\"E} {\\`I} ' + \
                u'{\\\'I} {\\^I} {\\"I} {\\DH} {\\~N} {\\`O} {\\\'O} {\\^O} {\\~O} {\\"O} {\\texttimes} {\\O} {\\`U} {\\\'U} {\\^U} ' + \
                u'{\\"U} {\\\'Y} {\\TH} {\\ss} ' + \
                u'{\\`a} {\\\'a} {\\^a} {\\~a} {\\"a} {\\r{a}} {\\ae} {\\c{c}} {\\`e} {\\\'e} {\\^e} {\\"e} {\\`\\i} {\\\'\\i} ' + \
                u'{\\^\\i} {\\"\\i} {\\dh} {\\~n} {\\`o} {\\\'o} {\\^o} {\\~o} {\\"o} {\\textdiv} {\\o} {\\`u} {\\\'u} {\\^u} {\\"u} ' + \
                u'{\\\'y} {\\th} {\\"y}'
        assert (utf8tolatex(text, ascii_no_brackets=True) == latex)


    def test_latin_extended_a(self):
        text = u'Ā ā Ă ă Ą ą Ć ć Ĉ ĉ Ċ ċ Č č Ď ď Đ đ Ē ē Ĕ ĕ Ė ė Ę ę Ě ě Ĝ ĝ Ğ ğ Ġ ġ Ģ ģ ' + \
               u'Ĥ ĥ Ħ ħ Ĩ ĩ Ī ī Ĭ ĭ Į į İ ı Ĳ ĳ Ĵ ĵ Ķ ķ ĸ Ĺ ĺ Ļ ļ Ľ ľ Ŀ ŀ Ł ł Ń ń Ņ ņ Ň ň ŉ ' + \
               u'Ŋ ŋ Ō ō Ŏ ŏ Ő ő Œ œ Ŕ ŕ Ŗ ŗ Ř ř Ś ś Ŝ ŝ Ş ş Š š Ţ ţ Ť ť Ŧ ŧ Ũ ũ Ū ū Ŭ ŭ Ů ů Ű ű ' + \
               u'Ų ų Ŵ ŵ Ŷ ŷ Ÿ Ź ź Ż ż Ž ž ſ'
        latex = u'{\\={A}} {\\={a}} {\\u{A}} {\\u{a}} {\\k{A}} {\\k{a}} {\\\'C} {\\\'c} {\\^{C}} {\\^{c}} ' + \
                u'{\\.{C}} {\\.{c}} {\\v{C}} {\\v{c}} {\\v{D}} {\\v{d}} {\\DJ} {\\dj} {\\={E}} {\\={e}} ' + \
                u'{\\u{E}} {\\u{e}} {\\.{E}} {\\.{e}} {\\k{E}} {\\k{e}} {\\v{E}} {\\v{e}} {\\^{G}} {\\^{g}} ' + \
                u'{\\u{G}} {\\u{g}} {\\.{G}} {\\.{g}} {\\c{G}} {\\c{g}} ' + \
                u'{\\^{H}} {\\^{h}} {\\={H}} {\\={h}} {\\~{I}} {\\~{i}} {\\={I}} {\\={\\i}} {\\u{I}} {\\u{i}} ' + \
                u'{\\k{I}} {\\k{i}} {\\.I} {\\i} {\\IJ} {\\ij} {\\^{J}} {\\^{j}} {\\c{K}} {\\c{k}} {\\textsc\\{k\\}} ' + \
                u'{\\\'L} {\\\'l} {\\c{L}} {\\c{l}} {\\v{L}} {\\v{l}} {\\.{L}} {\\.{l}} {\\L} {\\l} {\\\'N} {\\\'n} ' + \
                u'{\\c{N}} {\\c{n}} {\\v{N}} {\\v{n}} {\\\'n} ' + \
                u'{\\NG} {\\ng} {\\={O}} {\\={o}} {\\u{O}} {\\u{o}} {\\H{O}} {\\H{o}} {\\OE} {\\oe} {\\\'R} {\\\'r} ' + \
                u'{\\c{R}} {\\c{r}} {\\v{R}} {\\v{r}} {\\\'S} {\\\'s} {\\^{S}} {\\^{s}} {\\c{S}} {\\c{s}} {\\v{S}} {\\v{s}} ' + \
                u'{\\c{T}} {\\c{t}} {\\v{T}} {\\v{t}} {\\={T}} {\\={t}} {\\~{U}} {\\~{u}} {\\={U}} {\\={u}} {\\u{U}} {\\u{u}} ' + \
                u'{\\r{U}} {\\r{u}} {\\H{U}} {\\H{u}} ' + \
                u'{\\k{U}} {\\k{u}} {\\^{W}} {\\^{w}} {\\^{Y}} {\\^{y}} {\\"Y} {\\\'Z} {\\\'z} {\\.Z} {\\.z} {\\v{Z}} {\\v{z}} ſ'
        assert (utf8tolatex(text, ascii_no_brackets=True) == latex)


if __name__ == '__main__':
    unittest.main()
