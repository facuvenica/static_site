class HTMLNode:

    def __init__(self, tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props:
            retval = list(map(lambda key: f' {key}="{self.props[key]}"', self.props))

            return ''.join(retval)
        else:
            return ''
    
    def __repr__(self):
        return (f"Tag: {self.tag}, Value: {self.value}, "
                f"Children: {self.children}, Props: {self.props}")


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)


    def to_html(self):
        if self.value == None:
            raise ValueError('Value was not defined')

        if self.tag:
            props = self.props_to_html()
            return f"<{self.tag}{props}>{self.value}</{self.tag}>"
        else:
            return self.value
        

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError('Missing HTML tag')

        if not self.children:
            raise ValueError('ParentNode requires children')

        content = ''
        props = self.props_to_html()

        for child in self.children:
            content += child.to_html()

        return f"<{self.tag}{props}>{content}</{self.tag}>"