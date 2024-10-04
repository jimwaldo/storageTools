import extractList as el


class Storage_Summary:
    """
    A class to hold the summary of storage use for a particular kind of storage. The building of the object occurs
    on initialization, but could also be done separately via build_from_list().
    """
    def __init__(self, store_name, i, store_l):
        self.storageName = store_name
        self.total, self.distribution = el.get_distribution(store_l, i)
        sort_list = sorted(store_l, key=lambda x:x[i], reverse=True)
        self.num_users = 0
        for l in sort_list:
            if l[i] > 0:
                self.num_users += 1

        top_twenty = sort_list[:20]
        self.top_twenty_total = 0
        self.top_twenty = []
        for t in top_twenty:
            tt_entry = t[1:-6]
            tt_entry.append(t[i])
            self.top_twenty_total += t[i]
            self.top_twenty.append(tt_entry)
        return None

    def build_from_list(self, store_name, i, store_l):
        """
        Build the storage summary for the data in store_l
        :param store_name: The name of the storage
        :param i: The index of the storage data in store_l
        :param store_l: A list of lists with the storage data
        :return: None
        """
        self.storageName = store_name
        self.total, self.distribution = el.get_distribution(store_l, i)
        top_twenty = sorted(store_l, key=lambda x: x[i], reverse=True)[:20]
        for t in top_twenty:
            tt_entry = t[1:-6]
            tt_entry.append(t[i])
            self.top_twenty_total += t[i]
            self.top_twenty.append(tt_entry)

        return None

    def print_summary(self):
        """
        Print the summary of the storage use. While this currently prints to std.out, the intention is that the
        output can be redirected to a file.
        :return:
        """
        print('Storage Summary for {}'.format(self.storageName))
        print('Total storage used: {}'.format(self.total))
        print('Total number of users: {}'.format(self.num_users))
        print('Top 20 Total Use: {}'.format(self.top_twenty_total))
        print('Distribution of storage use:')
        print('\tLess than 1GB: {}'.format(self.distribution[0]))
        print('\t1-10GB: {}'.format(self.distribution[1]))
        print('\t10-100GB: {}'.format(self.distribution[2]))
        print('\t100-1000GB: {}'.format(self.distribution[3]))
        print('\tOver 1000GB: {}'.format(self.distribution[4]))
        print('Top 20 users:')
        for u in self.top_twenty:
            print(u)
        print('\n')
        return None

