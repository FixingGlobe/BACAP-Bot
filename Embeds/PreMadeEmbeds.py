from Embeds.EmptyRequestEmbed import EmptyRequestEmbed

bad_request = EmptyRequestEmbed(title="Bad Request", description="This advancement doesn't exist!")
bad_params = EmptyRequestEmbed(title="Advancement not found!",
                               description="There aren't any advancements with such parameters.")
