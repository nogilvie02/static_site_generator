from textnode import TextNode, TextType

def __main__():
    test_text_node = TextNode("this is a test", TextType.LINK, "https://www.boot.dev")
    print(test_text_node)
    
__main__()