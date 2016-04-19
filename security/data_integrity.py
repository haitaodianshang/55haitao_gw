#coding: utf8
from json import JSONEncoder
import md5, six, logging, copy

STATIC_SALT = '55haitao.com'
json_encoder = JSONEncoder()

def serialize(obj):
    if isinstance(obj, bool):
        return str(int(obj))
    elif isinstance(obj, six.string_types) or isinstance(obj, six.text_type):
        return obj
    elif isinstance(obj, six.integer_types):
        return str(int(obj))
    elif obj is None:
        return ''
    else:
        logging.error('没预料到的序列化类型:%s', obj)
        return str(obj)
    
def sign(se_level, data, dtk=None, tk=None):
    data = copy.copy(data)
    if '_sig' in data:
        data.pop('_sig')
    pair_list = []
    for key in sorted(data.keys()):
        pair_list.append('%s=%s' % (key, serialize(data[key])))
    if se_level == 2:
        salt = tk
        if tk is None:
            raise Exception('none tk')
    elif se_level == 1:
        salt = dtk
        if dtk is None:
            raise Exception('none dtk')
    elif se_level == 0:
        salt = STATIC_SALT
    else:
        raise Exception('未知安全级别')
    sign_str = '&'.join(pair_list) + salt

    if data.get('_sm', '') != 'MD5':
        raise Exception('不支持的签名方式')

    print sign_str

    signature = md5.new(sign_str).hexdigest()
    print signature
    return signature


if __name__ == '__main__':
    data = {
      "_aid": 1001,
      "_chl": "",
      "_cid": "D1750750-4E22-499F-9EEF-19B79C25E955_14598260491460010709",
      "_did": "D1750750-4E22-499F-9EEF-19B79C25E955_1459826049",
      "_dtk": "WHuXe+ov9212GVQ+ludmwDZbbuo44CdBfuG20ZpAYUOMeS1ZTCUx\/Ja3fD8UHaUQ3Bw7LFhBMSkhjC4+QpUqX3UTKUGXNIh4SqLtvFeFr10=",
      "_mt": "baijie_sns.TopicAPI\/get_topic_list",
      "_pl": "ios",
      "_sig": "18a9f734231496cba735bb9a0db2da9a",
        "_test": False,
      "_sm": "md5",
      "_tk": "Kcxx+oDdDsdzI5Aa79iYceN7x5gjfgy4UrcjQ9ljU19fXDhpV7TN\/0qjGwQH5AQCFAyc4HZgaMntgMVBb\/S6k99KyizBe8tak7OXLAFSOmWcnMU9\/h\/QbHX3zAEdBGyw",
      "_vc": "1.4",
      "count": 10,
      "key_word": "81540",
      "page": 1,
      "tag_id": 0,
      "type": 2
    }
    """data = {
    "_aid" = 1001;
    "_chl" = "";
    "_cid" = "13857697-BB87-44B1-AF44-599297EA6DCB_14593928861460024696";
    "_did" = "13857697-BB87-44B1-AF44-599297EA6DCB_1459392886";
    "_dtk" = "VUNdKllUSOIxgK+8qQcxAjiOz8JjTwiJ1wZ21TihmdjNR33xKkKj7rrx5HUDwSKQAQ0iPrIOoboWNmOsG11bpaE87efNhQtOhTJTSsd/ftU=";
    "_mt" = "baijie_sns.TopicAPI/get_topic_list";
    "_pl" = ios;
    "_sig" = null;
    "_sm" = MD5;
    "_tk" = "7BfeztHe19sT5/BTJlAeYGrJqs0pkggBn1y7DMzN4r3uK1XiDQClpe4Mo8gUifdfzI57+6DaEo7TA1BHuNXncgn30VL9rnheiXXZVLCqpMZCN6bxOrGtDU/bWGTx4eSd";
    "_vc" = "1.4";
    count = 10;
    "key_word" = 72056;
    page = 1;
    "tag_id" = 0;
    type = 2;
}"""
    data = {
  "_aid": 1001,
  "_chl": "",
  "_cid": "D1750750-4E22-499F-9EEF-19B79C25E955_14598260491460032212",
  "_did": "D1750750-4E22-499F-9EEF-19B79C25E955_1459826049",
  "_dtk": "WHuXe+ov9212GVQ+ludmwDZbbuo44CdBfuG20ZpAYUOMeS1ZTCUx\/Ja3fD8UHaUQ3Bw7LFhBMSkhjC4+QpUqX3UTKUGXNIh4SqLtvFeFr10=",
  "_mt": "usercenter.DeviceService\/update_push_token",
  "_pl": "ios",
  "_sig": "8ebb590275a8865c579542192226e076",
  "_sm": "MD5",
  "_tk": "Kcxx+oDdDsdzI5Aa79iYceN7x5gjfgy4UrcjQ9ljU19fXDhpV7TN\/0qjGwQH5AQCscujtLl4D6lLxdedCJJjxRPXV1PgA\/69xa20XxT1YJKW\/ANmpwena1Wx\/WuZnWoz",
  "_vc": "1.4",
  "push_device_token": "171976fa8a8309ea2f1"
}


    assert sign(1, data, dtk='WHuXe+ov9212GVQ+ludmwDZbbuo44CdBfuG20ZpAYUOMeS1ZTCUx\/Ja3fD8UHaUQ3Bw7LFhBMSkhjC4+QpUqX3UTKUGXNIh4SqLtvFeFr10=') == '1'
    assert sign('DeviceLogin', data, dtk='WHuXe+ov9212GVQ+ludmwDZbbuo44CdBfuG20ZpAYUOMeS1ZTCUx\/Ja3fD8UHaUQ3Bw7LFhBMSkhjC4+QpUqX3UTKUGXNIh4SqLtvFeFr10=') == '2'
    assert sign('None', data, '55haitao.com') == '2'
