import glob
import os
import json
import pandas as pd


def save_json(path, obj):
    with open(path+'tmp', 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    os.rename(path+'tmp', path)


def load_json(path):
    with open(path, 'r') as f:
        obj = json.load(f)
    return obj


class AppData(object):

    def __init__(self, auto_process=True):
        self.data_dir = './data/coinmarket/'
        self.data_files = []
        self.data_path = None
        self.tag_coins = {}
        self.coin_tags = {}
        self.data = {}
        self.data_df = None
        self.tag_info_df = None

        if auto_process:
            self.get_data_files()
            self.get_data()

    def get_data_files(self):
        d_files = glob.glob(os.path.join(self.data_dir, '*.json'))
        d_files.sort()
        d_files = d_files[::-1]
        self.data_files = d_files

    def get_data(self):
        self.data_path = self.data_files[0]
        self.data_df, self.data = self.read_data(self.data_path)
        self.tag_coins, self.coin_tags = self.get_tag_maps(self.data)
        self.tag_info_df = self.get_tag_info_df()

    def read_data(self, d_path):
        d = load_json(d_path)
        d_df = pd.DataFrame(d['data'])
        d_df['market_cap'] = d_df.quote.apply(lambda d: d['USD']['market_cap'])
        d_df['diluted_market_cap'] = d_df.quote.apply(lambda d: d['USD']['fully_diluted_market_cap'])
        return d_df, d

    @staticmethod
    def get_tag_maps(d):
        t_c = {}
        c_t = {}
        for d in d['data']:
            dis = '{}_{}'.format(d['id'], d['name'])
            c_t[dis] = d['tags']
            for tag in d['tags']:
                coins = t_c.get(tag)
                if coins:
                    coins.append(dis)
                else:
                    t_c[tag] = [dis]
        return t_c, c_t

    def get_tag_info_df(self):
        tag_info = {k: [len(self.tag_coins[k])] for k in self.tag_coins}

        for tag in self.tag_coins.keys():
            c_s = self.tag_coins[tag]
            c_s_id = [int(c.split('_')[0]) for c in c_s]
            v = self.data_df[self.data_df.id.isin(c_s_id)].market_cap.sum() / 10**8
            tag_info[tag].append(v)

        df = pd.DataFrame([[v[0]]+v[1] for v in tag_info.items()], columns=['tag', 'count', 'market_cap'])
        df = df.reset_index().drop(columns='index')
        df['tag_type'] = df.tag.apply(self.get_tag_type)

        return df

    @staticmethod
    def get_tag_type(tag_name):
        if 'ecosystem' in tag_name:
            return 'ecosystem'
        else:
            return 'default'


def get_app_data():
    app_data = AppData(auto_process=False)
    app_data.get_data_files()
    app_data.get_data()
    return app_data
