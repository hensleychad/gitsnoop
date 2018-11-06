from pydriller import RepositoryMining, GitRepository
from datetime import datetime, timezone, timedelta


def mineRepo( repoPath , branch):
    count = 0
    to_zone = timezone(timedelta(hours=5))
    dt1 = datetime(2003, 5, 1, 0, 0, 0, tzinfo=to_zone)
    dt2 = datetime(2017, 11, 1, 0, 0, 0, tzinfo=to_zone)

    for commit in RepositoryMining(
        repoPath, only_in_branch=branch,since=dt1, to=dt2).traverse_commits():
        count = count +1;
        for modification in commit.modifications:
            print('Branch {}, Author {}, modified {},date {}.commit {}'.format(branch, commit.author.name, modification.filename, commit.committer_date,commit.hash))
        print('Final Count ', count);

if __name__ == "__main__":
    repoPath = ('/Users/chensle/emse/SE6356.MS1-SoftwareMaintenanceEvolutionAndRe-Engineering-F18/Projects/local_repo/peep-commons-math' )
    branches = ["3.6-release", "3.6.1-release", "EXPERIMENTAL", "MANTISSA", "MATH-1153", "MATH_1_1",
               "MATH_1_1_RC1_tmp", "MATH_1_3", "MATH_2_0_tmp", "MATH_2_X", "MATH_3_X", "complex-and-primitive-arrays",
               "develop", "feature-MATH-1290", "feature-MATH-1333", "feature-MATH-1370", "feature-MATH-1372", "feature-MATH-1416",
               "field-ode", "fix-math-1342", "h10-builds", "master", "master-old", "task-MATH-1366"]
    gr = GitRepository(repoPath);

    for branch in branches:
      mineRepo(repoPath, branch)
