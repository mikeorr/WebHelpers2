import re
from string import Template

from webhelpers2.html import HTML, literal
import webhelpers2.html._render as render
from webhelpers2.html.tools import *

# I give up trying to convert all these eq_'s to plain asserts; there's too
# many of them and they're so long.

def eq_(a, b):
    assert a == b

class TestToolsHelper(object):
    
    def test_auto_link_parsing(self):
        urls = [
            literal("http://www.pylonshq.com"),
            literal("http://www.pylonshq.com:80"),
            literal("http://www.pylonshq.com/~minam"),
            literal("https://www.pylonshq.com/~minam"),
            literal("http://www.pylonshq.com/~minam/url%20with%20spaces"),
            literal("http://www.pylonshq.com/foo.cgi?something=here"),
            literal("http://www.pylonshq.com/foo.cgi?something=here&and=here"),
            literal("http://www.pylonshq.com/contact;new"),
            literal("http://www.pylonshq.com/contact;new%20with%20spaces"),
            literal("http://www.pylonshq.com/contact;new?with=query&string=params"),
            literal("http://www.pylonshq.com/~minam/contact;new?with=query&string=params"),
            literal("http://en.wikipedia.org/wiki/Wikipedia:Today%27s_featured_picture_%28animation%29/January_20%2C_2007"),
            literal("http://www.pylonshq.com/foo.cgi?date=01/01/01"),
            ]
        for url in urls:
            assert '<a href="%s">%s</a>' % (url, url) == auto_link(url)

    def test_auto_link_with_brackets(self):
        b = '[<a href="http://www.example.com">http://www.example.com</a>]'
        assert auto_link("[http://www.example.com]") == b

    def test_auto_linking(self):
        raw_values = {
            "email_raw": literal("david@loudthinking.com"),
            "link_raw": literal("http://www.pylonshq.com"),
            "link2_raw": literal("www.pylonshq.com"),
            "link3_raw": literal("http://manuals.we-love-the-moon.com/read/chapter.need_a-period/103#page281"),
            "link4_raw": literal("http://foo.example.com/controller/action?parm=value&p2=v2#anchor123"),
            "link5_raw": literal("http://foo.example.com:3000/controller/action"),
            "link6_raw": literal("http://foo.example.com:3000/controller/action+pack"),
            "link7_raw": literal("http://foo.example.com/controller/action?parm=value&p2=v2#anchor-123"),
            "link8_raw": literal("http://foo.example.com:3000/controller/action.html"),
            "link9_raw": literal("http://business.timesonline.co.uk/article/0,,9065-2473189,00.html")
            }

        result_values_templates = {
            "email_result":  '<a href="mailto:${email_raw}">${email_raw}</a>',
            "link_result":  '<a href="${link_raw}">${link_raw}</a>',
            "link_result_with_options":  '<a href="${link_raw}" target="_blank">${link_raw}</a>',
            "link2_result":  '<a href="http://${link2_raw}">${link2_raw}</a>',
            "link3_result":  '<a href="${link3_raw}">${link3_raw}</a>',
            "link4_result":  '<a href="${link4_raw}">${link4_raw}</a>',
            "link5_result":  '<a href="${link5_raw}">${link5_raw}</a>',
            "link6_result":  '<a href="${link6_raw}">${link6_raw}</a>',
            "link7_result":  '<a href="${link7_raw}">${link7_raw}</a>',
            "link8_result":  '<a href="${link8_raw}">${link8_raw}</a>',
            "link9_result":  '<a href="${link9_raw}">${link9_raw}</a>'
            }

        result_values = {}
        for k, v in result_values_templates.items():
            result_values[k] = Template(v).substitute(raw_values)

        eq_(result_values["email_result"], auto_link(raw_values["email_raw"], "email_addresses"))
        eq_("hello %(email_result)s" % result_values, auto_link("hello %(email_raw)s" % raw_values, "email_addresses"))
        eq_("Go to %(link_result)s" % result_values, auto_link("Go to %(link_raw)s" % raw_values, "urls"))
        eq_("Go to %(link_raw)s" % raw_values, auto_link("Go to %(link_raw)s" % raw_values, "email_addresses"))
        eq_("Go to %(link_result)s and say hello to %(email_result)s" % result_values, auto_link("Go to %(link_raw)s and say hello to %(email_raw)s" % raw_values))
        eq_("<p>Link %(link_result)s</p>" % result_values, auto_link(literal("<p>Link %(link_raw)s</p>") % raw_values))
        eq_("<p>%(link_result)s Link</p>" % result_values, auto_link(literal("<p>%(link_raw)s Link</p>") % raw_values))
        eq_("<p>Link %(link_result_with_options)s</p>" % result_values, auto_link(literal("<p>Link %(link_raw)s</p>") % raw_values, "all", target="_blank"))
        eq_("Go to %(link_result)s." % result_values, auto_link("Go to %(link_raw)s." % raw_values))
        eq_("<p>Go to %(link_result)s, then say hello to %(email_result)s.</p>" % result_values, auto_link(literal("<p>Go to %(link_raw)s, then say hello to %(email_raw)s.</p>") % raw_values))
        eq_("Go to %(link2_result)s" % result_values, auto_link("Go to %(link2_raw)s" % raw_values, "urls"))
        eq_("Go to %(link2_raw)s" % raw_values, auto_link("Go to %(link2_raw)s" % raw_values, "email_addresses"))
        eq_("<p>Link %(link2_result)s</p>" % result_values, auto_link(literal("<p>Link %(link2_raw)s</p>") % raw_values))
        eq_("<p>%(link2_result)s Link</p>" % result_values, auto_link(literal("<p>%(link2_raw)s Link</p>") % raw_values))
        eq_("Go to %(link2_result)s." % result_values, auto_link(literal("Go to %(link2_raw)s.") % raw_values))
        eq_("<p>Say hello to %(email_result)s, then go to %(link2_result)s.</p>" % result_values, auto_link(literal("<p>Say hello to %(email_raw)s, then go to %(link2_raw)s.</p>") % raw_values))
        eq_("Go to %(link3_result)s" % result_values, auto_link("Go to %(link3_raw)s" % raw_values, "urls"))
        eq_("Go to %(link3_raw)s" % raw_values, auto_link("Go to %(link3_raw)s" % raw_values, "email_addresses"))
        eq_("<p>Link %(link3_result)s</p>" % result_values, auto_link(literal("<p>Link %(link3_raw)s</p>") % raw_values))
        eq_("<p>%(link3_result)s Link</p>" % result_values, auto_link(literal("<p>%(link3_raw)s Link</p>") % raw_values))
        eq_("Go to %(link3_result)s." % result_values, auto_link("Go to %(link3_raw)s." % raw_values))
        eq_("<p>Go to %(link3_result)s. seriously, %(link3_result)s? i think I'll say hello to %(email_result)s. instead.</p>" % result_values, auto_link(literal("<p>Go to %(link3_raw)s. seriously, %(link3_raw)s? i think I'll say hello to %(email_raw)s. instead.</p>") % raw_values))
        eq_("<p>Link %(link4_result)s</p>" % result_values, auto_link(literal("<p>Link %(link4_raw)s</p>") % raw_values))
        eq_("<p>%(link4_result)s Link</p>" % result_values, auto_link(literal("<p>%(link4_raw)s Link</p>") % raw_values))
        eq_("<p>%(link5_result)s Link</p>" % result_values, auto_link(literal("<p>%(link5_raw)s Link</p>") % raw_values))
        eq_("<p>%(link6_result)s Link</p>" % result_values, auto_link(literal("<p>%(link6_raw)s Link</p>") % raw_values))
        eq_("<p>%(link7_result)s Link</p>" % result_values, auto_link(literal("<p>%(link7_raw)s Link</p>") % raw_values))
        eq_("Go to %(link8_result)s" % result_values, auto_link("Go to %(link8_raw)s" % raw_values, "urls"))
        eq_("Go to %(link8_raw)s" % raw_values, auto_link("Go to %(link8_raw)s" % raw_values, "email_addresses"))
        eq_("<p>Link %(link8_result)s</p>" % result_values, auto_link(literal("<p>Link %(link8_raw)s</p>") % raw_values))
        eq_("<p>%(link8_result)s Link</p>" % result_values, auto_link(literal("<p>%(link8_raw)s Link</p>") % raw_values))
        eq_("Go to %(link8_result)s." % result_values, auto_link("Go to %(link8_raw)s." % raw_values))
        eq_("<p>Go to %(link8_result)s. seriously, %(link8_result)s? i think I'll say hello to %(email_result)s. instead.</p>" % result_values, auto_link(literal("<p>Go to %(link8_raw)s. seriously, %(link8_raw)s? i think I'll say hello to %(email_raw)s. instead.</p>") % raw_values))
        eq_("Go to %(link9_result)s" % result_values, auto_link("Go to %(link9_raw)s" % raw_values, "urls"))
        eq_("Go to %(link9_raw)s" % raw_values, auto_link("Go to %(link9_raw)s" % raw_values, "email_addresses"))
        eq_("<p>Link %(link9_result)s</p>" % result_values, auto_link(literal("<p>Link %(link9_raw)s</p>") % raw_values))
        eq_("<p>%(link9_result)s Link</p>" % result_values, auto_link(literal("<p>%(link9_raw)s Link</p>") % raw_values))
        eq_("Go to %(link9_result)s." % result_values, auto_link("Go to %(link9_raw)s." % raw_values))
        eq_("<p>Go to %(link9_result)s. seriously, %(link9_result)s? i think I'll say hello to %(email_result)s. instead.</p>" % result_values, auto_link(literal("<p>Go to %(link9_raw)s. seriously, %(link9_raw)s? i think I'll say hello to %(email_raw)s. instead.</p>") % raw_values))
        eq_("", auto_link(None))
        eq_("", auto_link(""))
        # Failing test: PylonsHQ bug #657
        #eq_('&lt;<a href="http://www.google.com">www.google.com</a>&gt;', auto_link("<www.google.com>"))

    def test_strip_links(self):
        eq_("on my mind", strip_links("<a href='almost'>on my mind</a>"))
        eq_("on my mind", strip_links("<A href='almost'>on my mind</A>"))
        eq_("on my mind\nall day long",
                         strip_links("<a href='almost'>on my mind</a>\n<A href='almost'>all day long</A>"))



class TestURLHelper(object):
    def test_button_to_with_straight_url(self):
        eq_("<form action=\"http://www.example.com\" class=\"button-to\" method=\"POST\"><div><input type=\"submit\" value=\"Hello\" /></div></form>", 
               button_to("Hello", "http://www.example.com"))

    def test_button_to_with_query(self):
        eq_("<form action=\"http://www.example.com/q1=v1&amp;q2=v2\" class=\"button-to\" method=\"POST\"><div><input type=\"submit\" value=\"Hello\" /></div></form>", 
               button_to("Hello", "http://www.example.com/q1=v1&q2=v2"))

    def test_button_to_with_escaped_query(self):
        eq_("<form action=\"http://www.example.com/q1=v1&amp;q2=v2\" class=\"button-to\" method=\"POST\"><div><input type=\"submit\" value=\"Hello\" /></div></form>",
                         button_to("Hello", "http://www.example.com/q1=v1&q2=v2"))
    
    def test_button_to_with_query_and_no_name(self):
        eq_("<form action=\"http://www.example.com?q1=v1&amp;q2=v2\" class=\"button-to\" method=\"POST\"><div><input type=\"submit\" value=\"http://www.example.com?q1=v1&amp;q2=v2\" /></div></form>", 
               button_to(None, "http://www.example.com?q1=v1&q2=v2"))
    
    def test_button_to_enabled_disabled(self):
        eq_("<form action=\"http://www.example.com\" class=\"button-to\" method=\"POST\"><div><input type=\"submit\" value=\"Hello\" /></div></form>",
               button_to("Hello", "http://www.example.com", disabled=False))
        eq_("<form action=\"http://www.example.com\" class=\"button-to\" method=\"POST\"><div><input disabled=\"disabled\" type=\"submit\" value=\"Hello\" /></div></form>",
               button_to("Hello", "http://www.example.com", disabled=True))
    
    def test_button_to_with_method_delete(self):
        eq_("<form action=\"http://www.example.com\" class=\"button-to\" method=\"POST\"><div><input id=\"_method\" name=\"_method\" type=\"hidden\" value=\"DELETE\" /><input type=\"submit\" value=\"Hello\" /></div></form>", 
            button_to("Hello", "http://www.example.com", method="DELETE"))
        eq_("<form action=\"http://www.example.com\" class=\"button-to\" method=\"post\"><div><input id=\"_method\" name=\"_method\" type=\"hidden\" value=\"delete\" /><input type=\"submit\" value=\"Hello\" /></div></form>", 
            button_to("Hello", "http://www.example.com", method="delete"))

    def test_button_to_with_method_get(self):
        eq_("<form action=\"http://www.example.com\" class=\"button-to\" method=\"get\"><div><input type=\"submit\" value=\"Hello\" /></div></form>",
            button_to("Hello", "http://www.example.com", method="get"))
        eq_("<form action=\"http://www.example.com\" class=\"button-to\" method=\"GET\"><div><input type=\"submit\" value=\"Hello\" /></div></form>",
            button_to("Hello", "http://www.example.com", method="GET"))

    def test_button_to_with_img(self):
        eq_('<form action="/content/edit/3" class="button-to" method="POST"><div><input alt="Edit" src="/images/icon_delete.gif" type="image" value="Edit" /></div></form>',
                         button_to("Edit", "/content/edit/3", type="image", src="/images/icon_delete.gif"))
        eq_('<form action="/content/submit/3" class="button-to" method="POST"><div><input alt="Complete the form" src="submit.png" type="image" value="Submit" /></div></form>',
                         button_to("Submit", "/content/submit/3", type="image", src="submit.png", alt="Complete the form"))

    def test_mail_to(self):
        eq_('<a href="mailto:justin@example.com">justin@example.com</a>', mail_to("justin@example.com"))
        eq_('<a href="mailto:justin@example.com">Justin Example</a>', mail_to("justin@example.com", "Justin Example"))
        eq_('<a class="admin" href="mailto:justin@example.com">Justin Example</a>',
                         mail_to("justin@example.com", "Justin Example", class_="admin"))

    def test_mail_to_with_javascript(self):
        eq_("<script type=\"text/javascript\">\n//<![CDATA[\neval(unescape('%64%6f%63%75%6d%65%6e%74%2e%77%72%69%74%65%28%27%3c%61%20%68%72%65%66%3d%22%6d%61%69%6c%74%6f%3a%6d%65%40%64%6f%6d%61%69%6e%2e%63%6f%6d%22%3e%4d%79%20%65%6d%61%69%6c%3c%2f%61%3e%27%29%3b'))\n//]]>\n</script>", mail_to("me@domain.com", "My email", encode = "javascript"))

    def test_mail_to_with_options(self):
        eq_('<a href="mailto:me@example.com?cc=ccaddress%40example.com&amp;bcc=bccaddress%40example.com&amp;subject=This%20is%20an%20example%20email&amp;body=This%20is%20the%20body%20of%20the%20message.">My email</a>',
            mail_to("me@example.com", "My email", cc="ccaddress@example.com",
                    bcc="bccaddress@example.com", subject="This is an example email",
                    body="This is the body of the message."))

    def test_mail_to_with_img(self):
        eq_('<a href="mailto:feedback@example.com"><img src="/feedback.png" /></a>',
                        mail_to("feedback@example.com", HTML.literal('<img src="/feedback.png" />')))

    def test_mail_to_with_hex(self):
        eq_("<a href=\"&#109;&#97;&#105;&#108;&#116;&#111;&#58;%6d%65@%64%6f%6d%61%69%6e.%63%6f%6d\">My email</a>",
                         mail_to("me@domain.com", "My email", encode = "hex"))
        eq_("<a href=\"&#109;&#97;&#105;&#108;&#116;&#111;&#58;%6d%65@%64%6f%6d%61%69%6e.%63%6f%6d\">&#109;&#101;&#64;&#100;&#111;&#109;&#97;&#105;&#110;&#46;&#99;&#111;&#109;</a>",
                         mail_to("me@domain.com", None, encode = "hex"))

    def test_mail_to_with_replace_options(self):
        eq_('<a href="mailto:wolfgang@stufenlos.net">wolfgang(at)stufenlos(dot)net</a>',
                        mail_to("wolfgang@stufenlos.net", None, replace_at="(at)", replace_dot="(dot)"))
        eq_("<a href=\"&#109;&#97;&#105;&#108;&#116;&#111;&#58;%6d%65@%64%6f%6d%61%69%6e.%63%6f%6d\">&#109;&#101;&#40;&#97;&#116;&#41;&#100;&#111;&#109;&#97;&#105;&#110;&#46;&#99;&#111;&#109;</a>",
                         mail_to("me@domain.com", None, encode = "hex", replace_at = "(at)"))
        eq_("<a href=\"&#109;&#97;&#105;&#108;&#116;&#111;&#58;%6d%65@%64%6f%6d%61%69%6e.%63%6f%6d\">My email</a>",
                         mail_to("me@domain.com", "My email", encode = "hex", replace_at = "(at)"))
        eq_("<a href=\"&#109;&#97;&#105;&#108;&#116;&#111;&#58;%6d%65@%64%6f%6d%61%69%6e.%63%6f%6d\">&#109;&#101;&#40;&#97;&#116;&#41;&#100;&#111;&#109;&#97;&#105;&#110;&#40;&#100;&#111;&#116;&#41;&#99;&#111;&#109;</a>",
                         mail_to("me@domain.com", None, encode = "hex", replace_at = "(at)", replace_dot = "(dot)"))
        eq_("<script type=\"text/javascript\">\n//<![CDATA[\neval(unescape('%64%6f%63%75%6d%65%6e%74%2e%77%72%69%74%65%28%27%3c%61%20%68%72%65%66%3d%22%6d%61%69%6c%74%6f%3a%6d%65%40%64%6f%6d%61%69%6e%2e%63%6f%6d%22%3e%4d%79%20%65%6d%61%69%6c%3c%2f%61%3e%27%29%3b'))\n//]]>\n</script>",
                         mail_to("me@domain.com", "My email", encode = "javascript", replace_at = "(at)", replace_dot = "(dot)"))


class TestHighlightHelper(object):
    def test_highlight(self):
        eq_("This is a <strong class=\"highlight\">beautiful</strong> morning",
                         highlight("This is a beautiful morning", "beautiful"))
        eq_(
            "This is a <strong class=\"highlight\">beautiful</strong> morning, but also a <strong class=\"highlight\">beautiful</strong> day",
            highlight("This is a beautiful morning, but also a beautiful day", "beautiful"))
        eq_("This text is not changed because we supplied an empty phrase",
                         highlight("This text is not changed because we supplied an empty phrase",
                                   None))

    def test_highlight_with_regex(self):
        eq_("This is a <strong class=\"highlight\">beautiful!</strong> morning",
                     highlight("This is a beautiful! morning", "beautiful!"))

        eq_("This is a <strong class=\"highlight\">beautiful! morning</strong>",
                     highlight("This is a beautiful! morning", "beautiful! morning"))

        eq_("This is a <strong class=\"highlight\">beautiful? morning</strong>",
                     highlight("This is a beautiful? morning", "beautiful? morning"))

    def test_highlight_phrases(self):
        eq_('The c<strong class="highlight">at</strong> in the h<strong class="highlight">at</strong>.',
            highlight("The cat in the hat.", "at"))
        eq_('The <strong class="highlight">cat</strong> in the <strong class="highlight">hat</strong>.',
            highlight("The cat in the hat.", ["cat", "hat"]))
        eq_('The <strong class="highlight">cat</strong> is <strong class="highlight">cut</strong>.',
            highlight("The cat is cut.", re.compile(R"c.t")))

    def test_highlight_args(self):
        eq_('The c<strong class="highlight">at</strong> in the h<strong class="highlight">at</strong>.',
            highlight("The cat in the hat.", "AT"))
        eq_("The cat in the hat.",
            highlight("The cat in the hat.", "AT", case_sensitive=True))
        eq_('The c<strong style="color:red">at</strong> in the h<strong style="color:red">at</strong>.',
            highlight("The cat in the hat.", "at", class_=None,
                style="color:red"))

    def test_highlight_literal(self):
        eq_(literal('The &lt;red&gt; c<strong class="highlight">at</strong>.'),
            highlight("The <red> cat.", "at"))
        eq_(literal('The <red> c<strong class="highlight">at</strong>.'),
            highlight(literal("The <red> cat."), "at"))


class TestStripTagsHelper(object):
    def test_compare_strip_tags_to_sanitize(self):
        text = 'I <i>really</i> like <script language="javascript">NEFARIOUS CODE</script> steak!'
        assert strip_tags(text) == render.sanitize(text)


class TestNL2BR(object):
    def test_nl2br(self):
        assert "A B<br />\nC D<br />\n<br />\nE F" == nl2br("A B\nC D\r\n\r\nE F")

    def test_nl2br2(self):
        assert "&lt;strike&gt;W&lt;/strike&gt;<br />\nThe W" == \
            nl2br("<strike>W</strike>\nThe W")

    def test_nl2br3(self):
        assert "<strike>W</strike><br />\nThe W" == \
            nl2br(literal("<strike>W</strike>\nThe W"))


class TestTextToHTML(object):
    def test_text_to_html1(self):
        assert "<p>crazy\n cross\n platform linebreaks</p>" == \
            text_to_html("crazy\r\n cross\r platform linebreaks")

    def test_text_to_html2(self):
        assert "<p>crazy<br />\n cross<br />\n platform linebreaks</p>" == \
            text_to_html("crazy\r\n cross\r platform linebreaks", True)

    def test_text_to_html3(self):
        assert "<p>A paragraph</p>\n\n<p>and another one!</p>" == \
            text_to_html("A paragraph\n\nand another one!")

    def test_text_to_html4(self):
        assert "<p>A paragraph<br />\n With a newline</p>" == \
            text_to_html("A paragraph\n With a newline", True)

    def test_text_to_html5(self):
        assert "<p>A paragraph\n With a newline</p>" == \
            text_to_html("A paragraph\n With a newline", False)

    def test_text_to_html6(self):
        assert "<p>A paragraph\n With a newline</p>" == \
            text_to_html("A paragraph\n With a newline")

    def test_text_to_html7(self):
        assert "" == text_to_html(None)

class TestUpdateParams(object):
    def test_add_param(self):
        assert update_params("foo", new1="NEW1") == "foo?new1=NEW1"

    def test_modify_param(self):
        assert update_params("foo?p=1", p="2") == "foo?p=2"

    def test_delete_param(self):
        assert update_params("foo?p=1", p=None) == "foo"

    def test_modify_param_with_fragment(self):
        control = "http://example.com/foo?new1=NEW1#myfrag"
        result = update_params(
            "http://example.com/foo?new1=OLD1#myfrag", new1="NEW1")
        assert result == control

    def test_debug(self):
        control = ("http://example.com/foo", {"new1": "NEW1"}, "myfrag")
        result = update_params("http://example.com/foo?new1=OLD1#myfrag",
            new1="NEW1", _debug=True)
        assert result == control

    def add_param2(self):
        control = "http://www.mau.de?foo=2&brrr=3"
        result = update_params("http://www.mau.de?foo=2", brrr=3)
        assert result == control

    def add_multiple_values(self):
        control = "http://www.mau.de?foo=C&foo=D"
        result = update_params("http://www.mau.de?foo=A&foo=B", foo=["C", "D"])
        assert result == control
