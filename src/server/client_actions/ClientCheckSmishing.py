from src.server.network.ClientAction import ClientAction


class ClientCheckSmishing(ClientAction):
    def act(self, data, send):
        list_inbox = []
        list_sms = data.split("&*(")
        for i in range(len(list_sms)):
            sms_info = list_sms[i]
            address = sms_info.split("#^%")[0]
            body = sms_info.split("&*(")[1]
            list_inbox.append((address, body))

        print(list_inbox)
