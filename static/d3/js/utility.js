    /**
     * add new child after checking if the same named child already exist
     * @param parentNode
     * @param childNode
     */
    function addChildNode(parentNode, childNode) {
        var isRepeat = false;

        for (var i = 0; i < parentNode.children.length; i++) {
            if (parentNode.children[i].name === childNode.name && childNode && childNode.children[0]) {
                addChildNode(parentNode.children[i], childNode.children[0]);
                isRepeat = true;
            }
        }

        if (!isRepeat) {
            parentNode.children.push(childNode);
        }
    }
