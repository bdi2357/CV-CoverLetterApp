# scripts.sh
git submodule deinit -f --all
rm -rf .git/modules/CoverLetterGen
rm -rf CoverLetterGen
git submodule add https://github.com/bdi2357/CoverLetterGen CoverLetterGen
git submodule update --init --recursive