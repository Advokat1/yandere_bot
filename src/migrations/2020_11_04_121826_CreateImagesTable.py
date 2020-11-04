from orator.migrations import Migration


class CreateImagesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('images') as table:
            table.big_integer('id').unsigned()
            table.json('tags').nullable()
            table.string('author', 511).nullable()
            table.string('source', 511).nullable()
            table.string('file_url', 511).nullable()
            table.integer('score').nullable()
            table.string('rating', 30).nullable()
            table.boolean('is_rating_locked').default(True)
            table.boolean('has_children').default(True)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('images')
