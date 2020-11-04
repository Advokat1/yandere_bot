from orator.migrations import Migration


class CreateUsersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('users') as table:
            table.big_integer('id').unsigned()
            table.string('first_name', 511).nullable()
            table.string('last_name', 511).nullable()
            table.string('username', 511)
            table.boolean('is_admin').default(False)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop_if_exists('users')
