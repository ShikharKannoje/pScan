from modules import *
from utility import *
from sklearn.ensemble.forest import RandomForestRegressor
__UPLOADS__ = "/root/pScan-Web/uploads/"

class ParkinsonsDiseaseHandler(RequestHandler):
    """
    Class to detect whether the person has Parkinson's Disease
    """

    def get(self):
        self.render("index.html")

    def post(self):

        # upload audio file in server
        voice = self.request.files["audio"][0]
        extn = os.path.splitext(voice['filename'])[1]
        fnm = os.path.splitext(voice['filename'])[0]
        cname = str(uuid.uuid4()) + extn
        fh = open(__UPLOADS__ + cname, 'w')
        fh.write(voice['body'])
        fh.close()

        # get features from the audio file
        attr = getAttributes(cname)
        fdf = mongoTolist(False)

        train = fdf[:,:-1]
        target = fdf[:,-1]

        #RandomForest Regression
        rf = RandomForestRegressor(n_estimators = 506, n_jobs = -1)
        rf.fit(train, target)

        updrs_val = rf.predict([attr])
        attr.append(updrs_val[0])

        # get the theta from database
        theta = list(db.theta.find({}))
        theta1 = theta[0]["theta1"]
        theta2 = theta[1]["theta2"]

        # check is the person has Parkinson's Disease
        isParkinson = octave.classify(theta1, theta2, np.array(attr))

        self.render("output.html", ipk = isParkinson, updrs = updrs_val[0])
        #self.write({"status" : "Successfull", "code" : 200, "isParkinson" : isParkinson, "UPDRS" : updrs[0], "features" : attr})
