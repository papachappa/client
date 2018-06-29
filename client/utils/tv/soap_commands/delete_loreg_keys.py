from utils.tv import soap_commands as sc


def delete_keys(tv):
    try:
        clientId = sc.connectFi(tv)
    except:
        raise

    k_list = ('/com/loewe',
              '/com/loewe/',
              '/com/loewe/*'
             )
    try:
        out = [sc.deleteLoregKey(tv, clientId, k).getResponse() for k in k_list]
    except:
        raise
    else:
        return out
