def group_by_prefix(df):
    grouped = df.groupby('Prefix')
    grouped_chunks = {
        prefix: group.drop(columns=['Prefix']) for prefix, group in grouped
    }
    return grouped_chunks
