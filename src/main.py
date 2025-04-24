from textnode import *

def main():
    new_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    #dup_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(new_node)
    #print(dup_node == new_node)

if __name__ == "__main__":
    main()