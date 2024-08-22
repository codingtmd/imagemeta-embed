
import argparse

from meta_gen import MetaReader, MetaWriter


class ArgParser:
    def get_args():
        """
        return arguments for ChatChain
        user can customize only parts of arguments, other arguments will be left for default
        Returns:
            args: arguments for ChatChain
        """
        parser = argparse.ArgumentParser(description='argparse')
        parser.add_argument('--mode', type=str, default="r",
                            help="read(r) or write(w) mode")
        parser.add_argument('--imagefile', type=str, default="",
                            help="file path of the target image")
        parser.add_argument('--metafile', type=str, default="",
                            help="file path of the meta data")
        parser.add_argument('--encrypt', type=int, default="0",
                            help="No(0) or Yes(1) for encryption")
        args = parser.parse_args()
        return args


### python image_meta_master.py --mode w --imagefile "./samples/月纱.png" --metafile "./samples/月纱.json"
### python image_meta_master.py --mode w --imagefile "./samples/月纱.png" --metafile "./samples/月纱.json" --encrypt 1

### python image_meta_master.py --mode r --imagefile "./samples/月纱_clone.png"

if __name__ == '__main__':
    args = ArgParser.get_args()

    if args.mode == "w":
        writer = MetaWriter(args.imagefile)
        writer.execute(args.metafile)
    elif args.mode == "r":
        reader = MetaReader(args.imagefile)
        reader.execute()
