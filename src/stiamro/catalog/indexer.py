from z3c.indexer.indexer import MultiIndexer

class NewsItemIndexer(MultiIndexer):

    def doIndex(self):

        # index text in textIndex
        if self.context.title or self.context.description:
            textIndex = self.getIndex('stiam.ro.text')
            textIndex.doIndex(self.oid, "%s %s" % (
                self.context.title, self.context.description))

        # index context in titleIndex
        if self.context.title:
            titleIndex = self.getIndex('stiam.ro.title')
            titleIndex.doIndex(self.oid, self.context.title)

        # index context in descriptionIndex
        if self.context.description:
            descriptionIndex = self.getIndex('stiam.ro.description')
            descriptionIndex.doIndex(self.oid, self.context.description)

        # index context in effective
        if self.context.updated:
            effectiveIndex = self.getIndex('stiam.ro.effective')
            effectiveIndex.doIndex(self.oid, self.context.updated)

        # index context in tags
        if self.context.tags:
            tagsIndex = self.getIndex('stiam.ro.tags')
            tagsIndex.doIndex(self.oid, self.context.tags)

        # index site source
        site = self.context.__parent__.__parent__.__name__
        sourceIndex = self.getIndex('stiam.ro.source')
        sourceIndex.doIndex(self.oid, site)

    def doUnIndex(self):

        # unindex text in textIndex
        textIndex = self.getIndex('stiam.ro.text')
        textIndex.doUnIndex(self.oid)

        # unindex context in titleIndex
        titleIndex = self.getIndex('stiam.ro.title')
        titleIndex.doUnIndex(self.oid)

        # unindex context in descriptionIndex
        descriptionIndex = self.getIndex('stiam.ro.description')
        descriptionIndex.doUnIndex(self.oid)

        # unindex context in effective
        effectiveIndex = self.getIndex('stiam.ro.effective')
        effectiveIndex.doUnIndex(self.oid)

        # unindex context in tags
        tagsIndex = self.getIndex('stiam.ro.tags')
        tagsIndex.doUnIndex(self.oid)

        sourceIndex = self.getIndex('stiam.ro.source')
        sourceIndex.doUnIndex(self.oid)
