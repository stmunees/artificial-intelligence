class Utility:
    @staticmethod
    def printKeys(dict):
        for key, value in dict.items() :
            print(key,end =",")
        print()
    @staticmethod
    def printLegalMoves(list):
        print(list,sep =",")
