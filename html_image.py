import imgkit

imgkit.from_url('http://google.com', 'out.jpg')
imgkit.from_file('test.html', 'out.jpg')
imgkit.from_string('Hello!', 'out.jpg')


if __name__ == '__main__':
    AVATAR = "https://platform-lookaside.fbsbx.com/platform/profilepic/" \
             "?asid=10156184859638719&height=100&width=100&ext=1559899617&hash=AeQTBogsP-yCDOQq"

    CATEGORY = "https://d3k9eq2976l0ly.cloudfront.net/images/1558678576.png"

    DEFAULT_AVATAR = "https://d38qg0g88iwzaq.cloudfront.net/images/1551953912.png"