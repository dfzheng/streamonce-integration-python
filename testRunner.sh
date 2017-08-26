echo "test Starting"
#python -c "from testRunnerHelper import createEmailTestGroup; createEmailTestGroup()" && echo -e "shell:\tcreate group finished"
python -m unittest && echo "test finished"
#python -c "from testRunnerHelper import deleteEmailTestGroup; deleteEmailTestGroup()" && echo -e "shell:\tdelete group and emails finished"
