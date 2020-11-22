from orator.migrations import Migration


class AddResourceId(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('images') as table:
            table.string('resource_id', 511).nullable()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('images') as table:
            table.drop_column('resource_id')
